from app.services.llm.router import get_llm
import logfire

llm = get_llm("cheap")


def rewrite_query(query, conversation_history):

    if not conversation_history:
        return query

    prompt = f"""
You are a query rewriting assistant.

Conversation History:
{conversation_history}

Current User Question:
{query}

Rewrite the user's question into a standalone search query.

Rules:
- Resolve pronouns.
- Preserve meaning.
- Return only the rewritten query.
"""

    response = llm.invoke(prompt)

    rewritten_query = response.content.strip()
    print("\n===== REWRITTEN QUERY =====")
    print(rewritten_query)
    print("===========================\n")

    logfire.info(f"Rewritten Query: {rewritten_query}")

    return rewritten_query