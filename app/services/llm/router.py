import logfire

from app.services.llm.gemini import get_gemini
from app.services.llm.groq import get_groq


def _is_quota_error(error: Exception) -> bool:
    text = str(error).lower()

    return (
        "resource_exhausted" in text
        or "429" in text
        or "quota" in text
    )


class RoutedLLM:
    def __init__(self):
        self.primary = get_gemini()
        self.fallback = get_groq()

    def invoke(self, prompt):
        try:
            return self.primary.invoke(prompt)

        except Exception as e:

            if _is_quota_error(e):

                logfire.warning(
                    "Gemini quota exceeded. Falling back to Groq.",
                    error=str(e),
                )

                try:
                    return self.fallback.invoke(prompt)

                except Exception as groq_error:
                    logfire.error(
                        "Groq fallback failed.",
                        error=str(groq_error),
                    )
                    raise

            raise


def get_llm(task="best"):
    if task == "cheap":
        return get_groq()

    return RoutedLLM()