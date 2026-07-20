from app.services.retrieval.prompt_builder import build_prompt
from app.services.retrieval.qdrant_service import search

question = input("Question: ")

results = search(question)

prompt = build_prompt(question, results)

print(prompt)
