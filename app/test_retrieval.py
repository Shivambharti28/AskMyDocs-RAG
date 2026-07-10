from app.services.retrieval.qdrant_service import search

question = input("Question: ")

results = search(question)

for i, r in enumerate(results, start=1):
    print("=" * 60)
    print(f"Rank: {i}")
    print(f"Score: {r['score']:.4f}")
    print(f"Source: {r['source']}")
    print(f"Page: {r['page']}")
    print(r["text"])