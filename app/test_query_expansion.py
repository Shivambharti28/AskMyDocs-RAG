from app.services.retrieval.query_expansion import expand_query

question = input("Question: ")

queries = expand_query(question)

print()

for q in queries:
    print(q)