from app.services.llm.gemini import get_gemini
from app.services.llm.groq import get_groq


class RoutedLLM:
    def __init__(self):
        self.primary = get_gemini()
        self.fallback = get_groq()

    def invoke(self, prompt):
        try:
            return self.primary.invoke(prompt)
        except Exception:
            return self.fallback.invoke(prompt)


def get_llm(task="best"):
    if task == "cheap":
        return get_groq()

    return RoutedLLM()
