from app.services.retrieval.bm25_service import search_bm25

query = input("Question: ")

results = search_bm25(query)

print()

for i, chunk in enumerate(results, start=1):

    print("=" * 60)

    print("Rank :", i)

    print("Page :", chunk["page"])

    print("Chunk:", chunk["chunk_id"])

    print()

    print(chunk["text"][:400])
