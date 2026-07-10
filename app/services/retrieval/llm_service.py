import logfire

from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import settings


# Initialize Gemini only once
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0.2,
)


def generate_answer(prompt: str) -> str:
    """
    Send the prompt to Gemini and return the generated answer.

    Args:
        prompt: Fully constructed RAG prompt.

    Returns:
        Generated answer as a string.
    """

    with logfire.span(
        "🤖 LLM Generation",
        model="gemini-2.5-flash",
    ):

        try:

            logfire.info(
                "Sending prompt to Gemini",
                prompt_length=len(prompt),
            )

            response = llm.invoke(prompt)

            answer = response.content.strip()

            logfire.info(
                "Received LLM response",
                answer_length=len(answer),
            )

            return answer

        except Exception as e:

            logfire.error(
                "LLM generation failed",
                error=str(e),
            )

            return (
                "Sorry, I couldn't generate an answer at the moment. "
                "Please try again."
            )