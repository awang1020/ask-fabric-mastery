"""CLI: build (or rebuild) the Fabric Mastery vector index."""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

# Allow running as a script without installation
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.indexer import build_index, index_stats  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build or rebuild the Fabric Mastery vector index."
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Delete and rebuild the collection from scratch.",
    )
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    log = logging.getLogger("build_index")

    log.info("Starting indexing (rebuild=%s)", args.rebuild)
    report = build_index(rebuild=args.rebuild)

    log.info("Files indexed: %d", report.files_indexed)
    log.info("Chunks created: %d", report.nodes_created)
    if report.skipped:
        log.info("Skipped (unsupported): %d", len(report.skipped))
        for s in report.skipped:
            log.debug("  - %s", s)
    log.info("Stats: %s", index_stats())

    if report.files_indexed == 0:
        log.error("No files were indexed. Add documents under the data folder and retry.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
