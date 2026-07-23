import logfire

from app.services.llm.router import get_llm


llm = get_llm("best")


def generate_answer(prompt: str) -> str:
    with logfire.span(
        "🤖 LLM Generation",
        model="Gemini -> Groq Router",
    ):

        logfire.info(
            "Sending prompt",
            prompt_length=len(prompt),
        )

        response = llm.invoke(prompt)

        answer = response.content.strip()

        logfire.info(
            "Received LLM response",
            answer_length=len(answer),
        )

        return answer