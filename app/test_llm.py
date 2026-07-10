from app.services.retrieval.qdrant_service import search
from app.services.retrieval.prompt_builder import build_prompt
from app.services.retrieval.llm_service import generate_answer

question = input("Question: ")

chunks = search(question)

prompt = build_prompt(question, chunks)

answer = generate_answer(prompt)

print("\n")
print("=" * 80)
print("ANSWER")
print("=" * 80)
print(answer)