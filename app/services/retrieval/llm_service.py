import traceback

import logfire
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from app.config import settings

groq_llm = ChatGroq(
    model=settings.GROQ_MODEL,
    api_key=settings.GROQ_API_KEY,
    temperature=0.2,
)

# Initialize Gemini only once
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0.2,
)


def generate_answer(prompt: str) -> str:

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
            # traceback.print_exc()

            if (
                "RESOURCE_EXHAUSTED" in str(e)
                or "429" in str(e)
                or "quota" in str(e).lower()
            ):

                logfire.warning(
                    "Gemini quota exceeded. Falling back to Groq.",
                    error=str(e),
                )
                try:
                    response = groq_llm.invoke(prompt)
                    return response.content.strip()

                except Exception as groq_error:

                    traceback.print_exc()

                    logfire.error(
                        "Groq fallback failed",
                        error=str(groq_error),
                    )

                    return "Sorry, both Gemini and Groq are unavailable."

            # Any other Gemini error
            raise
