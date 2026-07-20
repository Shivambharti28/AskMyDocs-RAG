from app.services.retrieval.hybrid_search import hybrid_search

query = input("Question: ")

dense, bm25 = hybrid_search(query)

print("\n===== DENSE SEARCH =====")
for chunk in dense:
    print(f"Page={chunk['page']} | Chunk={chunk['chunk_id']}")

print("\n===== BM25 SEARCH =====")
for chunk in bm25:
    print(f"Page={chunk['page']} | Chunk={chunk['chunk_id']}")
