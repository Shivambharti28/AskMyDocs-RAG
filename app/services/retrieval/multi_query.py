import re

from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import settings


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0,
)


def generate_multi_queries(question: str):
    """
    Generate multiple search perspectives for one question.
    """

    prompt = f"""
You are helping a Retrieval-Augmented Generation (RAG) system.

Generate 5 DIFFERENT search queries that explore different aspects
of the user's question.

Do NOT simply rewrite the question.

Instead, think of different perspectives, concepts, related topics,
definitions, examples, types, applications, or theories.

Return ONLY the search queries.
One query per line.

Question:
{question}
"""

    response = llm.invoke(prompt)

    queries = [
        line.strip("- ").strip()
        for line in response.content.split("\n")
        if line.strip()
    ]

    seen = set()
    unique_queries = []

    for q in queries:

        normalized = re.sub(
            r"[^\w\s]",
            "",
            q.lower(),
        ).strip()

        if normalized not in seen:
            seen.add(normalized)
            unique_queries.append(q)

    return unique_queries