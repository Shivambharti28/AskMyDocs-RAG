import logfire

from app.services.llm.router import get_llm

llm = get_llm("cheap")


def rewrite_query(
    query,
    conversation_history,
    verbose=True,
):
    # No previous conversation → no rewriting needed
    if not conversation_history:
        return query

    # Convert conversation history into readable dialogue
    history_text = "\n".join(
        f"{message['role'].title()}: {message['content']}"
        for message in conversation_history
    )

    prompt = f"""
You are an expert search query rewriting assistant.

Your job is to rewrite the user's latest question into a standalone search query.

Conversation History:
{history_text}

Current User Question:
{query}

Instructions:
- Resolve pronouns such as "it", "they", "this", "that", "he", "she", etc.
- Use the conversation history to identify what those pronouns refer to.
- Preserve the user's original intent.
- Do not answer the question.
- Do not add extra information.
- Return only the rewritten standalone query.

Examples:

Conversation:
User: What is Retrieval-Augmented Generation?
Assistant: Retrieval-Augmented Generation (RAG) combines retrieval with LLM generation.

Question:
How does it work?

Output:
How does Retrieval-Augmented Generation work?

Conversation:
User: Explain BM25.
Assistant: BM25 is a keyword-based retrieval algorithm.

Question:
Explain it in two lines.

Output:
Explain BM25 in two lines.
"""

    response = llm.invoke(prompt)

    rewritten_query = response.content.strip()

    if verbose:
        print("\n===== REWRITTEN QUERY =====")
        print(rewritten_query)
        print("===========================\n")

    logfire.info(f"Rewritten Query: {rewritten_query}")

    return rewritten_query