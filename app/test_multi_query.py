from app.services.retrieval.multi_query import generate_multi_queries

question = input("Question: ")

queries = generate_multi_queries(question)

print()

for q in queries:
    print(q)
