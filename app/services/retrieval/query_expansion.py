from langchain_google_genai import ChatGoogleGenerativeAI
import re

from app.config import settings


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0,
)


def expand_query(question: str):
    """
    Generate multiple search queries for one question.
    """

    prompt = f"""
Generate 4 different search queries for the question below.

Return ONLY the queries.

Question:
{question}
"""

    response = llm.invoke(prompt)

    

    # queries = [
    #     line.strip("- ").strip()
    #     for line in response.content.split("\n")
    #     if line.strip()
    # ]
    queries = [
    line.strip("- ").strip()
    for line in response.content.split("\n")
    if line.strip()
    ]

    # Remove duplicates while preserving order
    seen = set()
    unique_queries = []

    for q in queries:
        # normalized = q.lower().strip()
        normalized = re.sub(r"[^\w\s]", "", q.lower()).strip()
        if normalized not in seen:
            seen.add(normalized)
            unique_queries.append(q)

    # Ensure the original user query is included
    # if question.lower().strip() not in seen:
    #     unique_queries.insert(0, question)
    # Ensure the original user query is included
    normalized_question = re.sub(
        r"[^\w\s]",
        "",
        question.lower(),
    ).strip()

    if normalized_question not in seen:
        unique_queries.insert(0, question)

    return unique_queries

    # return queries