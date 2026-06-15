"""Local CLI smoke test for the RAG stack (used by pre-deploy validation)."""
from src.indexer import load_index, index_stats
from src.chat_engine import build_chat_engine, ask

stats = index_stats()
print("--- INDEX ---")
print(stats)

idx = load_index()
assert idx is not None, "Index not loaded - run scripts/build_index.py first"

eng = build_chat_engine(idx, language="fr")
r = ask(eng, "Quels sont les bonnes pratiques pour la sécurité dans Fabric ?")
print("\n--- ANSWER (first 400 chars) ---")
print(r.answer[:400])
print(f"\n--- SOURCES ({len(r.sources)}) ---")
for s in r.sources[:5]:
    url = s.url or "(no url)"
    print(f"  - {s.title or s.file_name}  ({s.date})  -> {url}")

