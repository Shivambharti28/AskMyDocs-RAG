import logfire

from app.services.retrieval.rag_pipeline import ask

logfire.configure(service_name="enterprise-rag")

question = input("Question: ")

source = input("Source (leave blank for all documents): ").strip()
page = input("Page (leave blank for all pages): ").strip()

result = ask(
    question=question,
    source=source if source else None,
    page=int(page) if page else None,
)

print("\n")
print("=" * 80)
print("ANSWER")
print("=" * 80)
print(result["answer"])

print("\n")
print("=" * 80)
print("SOURCES")
print("=" * 80)

for i, src in enumerate(result["sources"], start=1):
    print(f"\n{i}.")
    print("Document :", src.get("source"))
    print("Page     :", src.get("page"))
    print("Original Score :", round(src.get("score", 0), 4))

    if "rrf_score" in src:
        print("RRF Score      :", round(src["rrf_score"], 5)) 