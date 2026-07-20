import logfire

from app.services.retrieval.rag_pipeline import ask

logfire.configure(service_name="enterprise-rag")

print("=" * 80)
print("Enterprise RAG Chat")
print("Type 'exit' or 'quit' to end the conversation.")
print("=" * 80)

while True:

    question = input("\nQuestion: ").strip()

    if question.lower() in ["exit", "quit"]:
        print("\nGoodbye!")
        break

    source = input("Source (leave blank for all documents): ").strip()
    page = input("Page (leave blank for all pages): ").strip()

    result = ask(
        question=question,
        source=source if source else None,
        page=int(page) if page else None,
        verbose=True,
    )

    print("\n")
    print("=" * 80)
    print("ANSWER")
    print("=" * 80)
    print(result["answer"])

    # -----------------------------
    # Confidence
    # -----------------------------
    confidence = result.get("confidence")

    if confidence:
        print("\n")
        print("=" * 80)
        print("CONFIDENCE")
        print("=" * 80)
        print(f"Level : {confidence.get('level')}")
        print(f"Score : {confidence.get('score'):.1f}%")
        print(f"Top Similarity : {confidence.get('top_score'):.4f}")
        print(f"Average Similarity : {confidence.get('average_score'):.4f}")

    # -----------------------------
    # Sources
    # -----------------------------
    print("\n")
    print("=" * 80)
    print("SOURCES")
    print("=" * 80)

    for i, src in enumerate(result["sources"], start=1):

        print(f"\n{i}.")
        print("Document :", src.get("source"))
        print("Page     :", src.get("page"))

        dense = src.get("score")
        bm25 = src.get("bm25_score")

        if dense is not None:
            print(f"Dense Score    : {dense:.4f}")

        if bm25 is not None and bm25 > 0:
            print(f"BM25 Score     : {bm25:.4f}")

        if "rrf_score" in src:
            print(f"RRF Score      : {src['rrf_score']:.5f}")

        if "rerank_score" in src:
            print(f"Rerank Score   : {src['rerank_score']:.4f}")
