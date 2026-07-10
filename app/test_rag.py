import logfire

from app.services.retrieval.rag_pipeline import ask

logfire.configure(service_name="enterprise-rag")

question = input("Question: ")

result = ask(question)

print("\n")
print("=" * 80)
print("ANSWER")
print("=" * 80)
print(result["answer"])

print("\n")
print("=" * 80)
print("SOURCES")
print("=" * 80)

for i, source in enumerate(result["sources"], start=1):

    print(f"\n{i}.")

    print("Document :", source.get("source"))

    print("Page     :", source.get("page"))

    print("Score    :", round(source.get("score", 0), 4))