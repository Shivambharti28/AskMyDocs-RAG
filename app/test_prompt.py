from app.services.retrieval.qdrant_service import search
from app.services.retrieval.prompt_builder import build_prompt

question = input("Question: ")

results = search(question)

prompt = build_prompt(question, results)

print(prompt)