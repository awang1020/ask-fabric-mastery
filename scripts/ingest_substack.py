"""Ingest posts from a Substack publication into ./data/newsletters as Markdown.

Default source: https://antoinewang.substack.com (Fabric Mastery).

Strategy:
  1. Fetch /sitemap.xml to enumerate every published post URL.
  2. For each post, fetch the public HTML, isolate the article body
     (<div class="body markup"> or <article>), and convert to Markdown.
  3. Save as ``<YYYY-MM-DD>_<slug>.md`` with a YAML-style front-matter so
     LlamaIndex can surface title / URL / date as metadata.

The script is idempotent: existing files are skipped unless --force is set.
"""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
import time
from dataclasses import dataclass
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import get_settings  # noqa: E402

log = logging.getLogger("ingest_substack")

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)
DEFAULT_SUBSTACK = "https://antoinewang.substack.com"
POST_PATH_RE = re.compile(r"/p/[^/]+/?$")
SLUG_SANITIZE_RE = re.compile(r"[^a-z0-9-]+")
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


@dataclass
class Post:
    url: str
    slug: str
    title: str
    date: str  # ISO-8601 yyyy-mm-dd
    author: str
    markdown: str
    paywalled: bool


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update(
        {
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
            # Brotli (br) intentionally omitted: requests can't decode it without
            # the `brotli`/`brotlicffi` package, which would return raw bytes
            # masquerading as HTML and break every parser.
            "Accept-Encoding": "gzip, deflate",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        }
    )
    return s


def _fetch(session: requests.Session, url: str, *, timeout: int = 30, retries: int = 3) -> str:
    last_exc: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            resp = session.get(url, timeout=timeout, allow_redirects=True)
            resp.raise_for_status()
            return resp.text
        except requests.HTTPError as exc:
            last_exc = exc
            if resp.status_code in (403, 429, 503) and attempt < retries:
                wait = 2 * attempt
                log.warning("HTTP %s on %s — retry %d/%d in %ds", resp.status_code, url, attempt, retries, wait)
                time.sleep(wait)
                continue
            raise
        except requests.RequestException as exc:
            last_exc = exc
            if attempt < retries:
                time.sleep(2 * attempt)
                continue
            raise
    assert last_exc is not None
    raise last_exc


def list_post_urls(session: requests.Session, base_url: str) -> list[str]:
    base = base_url.rstrip("/")
    sitemap_url = f"{base}/sitemap.xml"
    log.info("Reading sitemap %s", sitemap_url)
    xml = _fetch(session, sitemap_url)
    root = ET.fromstring(xml)
    urls: list[str] = []
    for loc in root.findall(".//sm:url/sm:loc", SITEMAP_NS):
        if loc.text and POST_PATH_RE.search(urlparse(loc.text).path):
            urls.append(loc.text.strip())
    if not urls:
        log.warning("Sitemap returned no post URLs — falling back to /feed (last ~20 posts)")
        urls = list(_feed_url_date_map(session, base).keys())
    log.info("Found %d post URL(s)", len(urls))
    return sorted(set(urls))


def _feed_url_date_map(session: requests.Session, base: str) -> dict[str, str]:
    """Return {post_url: ISO-8601 date} pulled from the RSS feed."""
    try:
        feed = _fetch(session, f"{base}/feed")
    except Exception as exc:
        log.warning("Could not load /feed for date enrichment: %s", exc)
        return {}
    try:
        root = ET.fromstring(feed)
    except ET.ParseError as exc:
        log.warning("Could not parse /feed XML: %s", exc)
        return {}
    mapping: dict[str, str] = {}
    for item in root.findall(".//item"):
        link = item.find("link")
        pub = item.find("pubDate")
        if link is None or not link.text:
            continue
        url = link.text.strip()
        iso = ""
        if pub is not None and pub.text:
            try:
                iso = parsedate_to_datetime(pub.text).date().isoformat()
            except Exception:  # noqa: BLE001
                pass
        mapping[url] = iso
    return mapping


def _list_post_urls_from_feed(session: requests.Session, base: str) -> list[str]:
    return list(_feed_url_date_map(session, base).keys())


def _sanitize_slug(s: str) -> str:
    s = s.lower().strip()
    s = SLUG_SANITIZE_RE.sub("-", s).strip("-")
    return s[:80] or "post"


def parse_post(html: str, url: str, *, fallback_date: str = "") -> Post:
    soup = BeautifulSoup(html, "lxml")

    title_tag = soup.find("h1", class_="post-title") or soup.find("h1")
    title = (title_tag.get_text(strip=True) if title_tag else "Untitled").strip()

    iso_date = fallback_date
    if not iso_date:
        for sel in [
            ('meta', {'property': 'article:published_time'}),
            ('meta', {'name': 'parsely-pub-date'}),
        ]:
            tag = soup.find(*sel)
            if tag and tag.get('content'):
                iso_date = tag['content'][:10]
                break
    if not iso_date:
        date_tag = soup.find("time")
        if date_tag and date_tag.get("datetime"):
            iso_date = date_tag["datetime"][:10]

    author_tag = soup.find("a", class_="navLink") or soup.find("meta", attrs={"name": "author"})
    if author_tag and author_tag.name == "meta":
        author = (author_tag.get("content") or "").strip()
    elif author_tag:
        author = author_tag.get_text(strip=True)
    else:
        author = ""

    body = (
        soup.select_one("div.body.markup")
        or soup.select_one("div.available-content")
        or soup.select_one("div.body")
        or soup.select_one('div[class*="available-content"]')
        or soup.select_one('div[class*="post-content"]')
        or soup.select_one('div[class*="markup"]')
        or soup.select_one("article")
        or soup.select_one('div[class*="post"]')
    )
    if body is None:
        raise ValueError(f"No article body found at {url}")

    # Strip nuisance widgets (subscribe forms, share buttons, image grids)
    for sel in [
        "div.subscription-widget-wrap",
        "div.subscription-widget-wrap-editor",
        "div.image-link-expand",
        "div.captioned-image-container figure picture source",
        "button",
        "form",
        "script",
        "style",
        "svg",
    ]:
        for tag in body.select(sel):
            tag.decompose()

    markdown = md(str(body), heading_style="ATX", strip=["img"]).strip()
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)

    paywalled = bool(soup.find("div", class_="paywall"))

    slug = _sanitize_slug(urlparse(url).path.rsplit("/", 1)[-1])
    return Post(
        url=url,
        slug=slug,
        title=title,
        date=iso_date,
        author=author,
        markdown=markdown,
        paywalled=paywalled,
    )


def _render(post: Post) -> str:
    fm_lines = [
        "---",
        f"title: {post.title.replace(chr(10), ' ')}",
        f"url: {post.url}",
        f"date: {post.date}",
        f"author: {post.author}",
        f"source: substack",
        "---",
        "",
        f"# {post.title}",
        "",
        post.markdown,
        "",
    ]
    return "\n".join(fm_lines)


def _target_path(out_dir: Path, post: Post) -> Path:
    prefix = post.date or "undated"
    return out_dir / f"{prefix}_{post.slug}.md"


SOURCES_INDEX_FILENAME = "_sources_index.json"


def _load_existing_index(out_dir: Path) -> dict[str, dict[str, str]]:
    path = out_dir / SOURCES_INDEX_FILENAME
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        log.warning("Could not load existing %s (%s); starting fresh.", path.name, exc)
        return {}


def _write_sources_index(out_dir: Path, mapping: dict[str, dict[str, str]]) -> None:
    path = out_dir / SOURCES_INDEX_FILENAME
    path.write_text(json.dumps(mapping, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    log.info("Wrote sources index: %s (%d entries)", path.name, len(mapping))


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest Substack posts as Markdown.")
    parser.add_argument("--url", default=DEFAULT_SUBSTACK, help="Substack base URL.")
    parser.add_argument("--limit", type=int, default=0, help="Max posts to fetch (0 = all).")
    parser.add_argument("--force", action="store_true", help="Re-download existing posts.")
    parser.add_argument("--skip-paywalled", action="store_true", help="Skip preview-only posts.")
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds between requests.")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    out_dir: Path = get_settings().data_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    log.info("Output directory: %s", out_dir)

    session = _session()
    existing_md = sorted(out_dir.glob("*.md"))
    try:
        urls = list_post_urls(session, args.url)
    except requests.HTTPError as exc:
        status = getattr(exc.response, "status_code", "?")
        log.warning("Substack unreachable (HTTP %s) from this environment.", status)
        if existing_md:
            log.warning(
                "Falling back to %d previously-ingested posts already on disk.",
                len(existing_md),
            )
            return 0
        log.error("No local posts available and Substack is unreachable — aborting.")
        return 1

    url_dates = _feed_url_date_map(session, args.url.rstrip("/"))
    if args.limit > 0:
        urls = urls[: args.limit]

    sources_index: dict[str, dict[str, str]] = _load_existing_index(out_dir)
    saved = skipped = failed = paywalled = 0
    for i, url in enumerate(urls, start=1):
        try:
            html = _fetch(session, url)
            post = parse_post(html, url, fallback_date=url_dates.get(url, ""))
        except Exception as exc:  # noqa: BLE001 — log + continue
            log.error("[%d/%d] %s — FAIL: %s", i, len(urls), url, exc)
            failed += 1
            continue

        if post.paywalled and args.skip_paywalled:
            log.info("[%d/%d] %s — skipped (paywalled)", i, len(urls), url)
            paywalled += 1
            continue

        target = _target_path(out_dir, post)
        sources_index[target.name] = {
            "title": post.title,
            "url": post.url,
            "date": post.date,
            "author": post.author,
            "slug": post.slug,
        }

        if target.exists() and not args.force:
            log.info("[%d/%d] %s — already exists, skipped", i, len(urls), target.name)
            skipped += 1
            continue

        target.write_text(_render(post), encoding="utf-8")
        log.info("[%d/%d] saved %s (%.1f KB)", i, len(urls), target.name, target.stat().st_size / 1024)
        saved += 1
        time.sleep(args.delay)

    _write_sources_index(out_dir, sources_index)
    log.info(
        "Done — saved=%d skipped=%d paywalled=%d failed=%d total=%d",
        saved, skipped, paywalled, failed, len(urls),
    )
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
