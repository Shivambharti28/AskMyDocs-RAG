import logfire

MAX_CONTEXT_CHARS = 10000


# def build_prompt(question: str, retrieved_chunks: list[dict]) -> str:
def build_prompt(question: str,retrieved_chunks: list[dict],conversation_history: list[dict] | None = None,) -> str:

    with logfire.span("📝 Building Prompt",retrieved_chunks=len(retrieved_chunks),):
        # Remove duplicate chunks
        seen = set()
        unique_chunks = []

        for chunk in retrieved_chunks:
            text = chunk.get("text") or chunk.get("content", "")

            if text in seen:
                continue

            seen.add(text)
            unique_chunks.append(chunk)


        # System Instructions

        instruction = """

You are an Enterprise Retrieval-Augmented Generation (RAG) Assistant.

Your job is to answer ONLY from the retrieved context.

Rules:

1. Use ONLY the retrieved context.
2. Never use outside knowledge.
3. Never guess or fabricate facts.
4. Every factual statement must be supported by one or more retrieved sources.
5. Cite every factual statement.
6. Use ONLY the document names and page numbers provided in the retrieved context.
7. Never invent citations.
8. Never invent page numbers.
9. Never invent document names.
10. If multiple sources support the same statement, cite all of them.
11. If the answer is not supported by the retrieved context, reply exactly:
"I couldn't find this information in the provided documents."
12. If the retrieved documents disagree, clearly explain the disagreement.
13. Keep the answer concise, factual, and well structured.

Citation format:

(Document.pdf, p.5)

Examples:

Motivation is an internal process.
(Motivation_Psychology_Notes.pdf, p.2)

Motivation is influenced by biological and psychological factors.
(Motivation_Psychology_Notes.pdf, p.5; Motivation_Psychology_Notes.pdf, p.8)

"""

        # Build Conversation History

        history = ""

        if conversation_history:
            history += (
                "==================================================\n"
                    "CONVERSATION HISTORY\n"
                "==================================================\n\n"
            )
            for message in conversation_history:
                role = message["role"].upper()
                content = message["content"]
                history += f"{role}: {content}\n\n"
        else:
            history = (
                "==================================================\n"
                "CONVERSATION HISTORY\n"
                "==================================================\n\n"
                "No previous conversation.\n\n"
            )
        # Build Context
        context = ""
        for i, chunk in enumerate(unique_chunks, start=1):

            source = chunk.get("source", "Unknown")
            page = chunk.get("page", "Unknown")
            section = chunk.get("section")
            text = chunk.get("text") or chunk.get("content", "")

            # Skip empty chunks
            if not text.strip():
                continue

            # Show section only if meaningful
            section_text = ""
            if section and not str(section).startswith("Page"):
                section_text = f"\nSection : {section}"

            next_chunk = f"""
            ==================================================
            SOURCE {i}
            ==================================================

            Document : {source}
            Page     : {page}{section_text}

            Evidence:
            {text}

            --------------------------------------------------

            """


            # Prevent prompt from exceeding context budget
            if len(context) + len(next_chunk) > MAX_CONTEXT_CHARS:
                logfire.warning("Maximum context size reached.",max_context_chars=MAX_CONTEXT_CHARS,)
                break

            context += next_chunk
        # Final Prompt

        prompt = f"""
{instruction}

{history}

==================================================
RETRIEVED CONTEXT
==================================================

{context}

==================================================
CURRENT QUESTION
==================================================

{question}

==================================================
ANSWER
==================================================
"""


        logfire.info("Prompt built successfully.",unique_chunks=len(unique_chunks),context_length=len(context),prompt_length=len(prompt),)

        return prompt