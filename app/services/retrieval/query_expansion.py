from langchain_google_genai import ChatGoogleGenerativeAI

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

    queries = [
        line.strip("- ").strip()
        for line in response.content.split("\n")
        if line.strip()
    ]

    return queries