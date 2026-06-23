from dotenv import load_dotenv
from importlib.metadata import version

load_dotenv()

core_version = version("langchain-core")
lg_version = version("langgraph")

# from langchain_openai import ChatOpenAI
# from langchain_anthropic import ChatAnthropic
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

print(f"langchain-core version: {core_version}")
print(f"langgraph version: {lg_version}")


def main():
    # Test openai
    # llm_openai = ChatOpenAI(model_name = "gpt-4o-mini", temperature=0)
    # response_openai = llm_openai.invoke("Say 'setup complete!' in the word")
    # print(f"Response from ChatOpenAI: {response_openai}")

    # Test anthropic
    # llm_anthropic = ChatAnthropic(model_name = "claude-sonnet-4-5-20250929", temperature=0)
    # response_anthropic = llm_anthropic.invoke("Say 'setup complete!' in the word")
    # print(f"Response from ChatAnthropic: {response_anthropic}")

    #Test groq
    llm_groq = ChatGroq(model = "llama-3.3-70b-versatile",temperature=0)
    response_groq = llm_groq.invoke("Say 'setup complete!' in the word")
    print(f"Response from ChatGroq: {response_groq}")

    #Test gemini
    llm_gemini = ChatGoogleGenerativeAI(model = "gemini-2.5-flash", temperature = 0)
    response_gemini = llm_gemini.invoke("Say 'setup complete!' in the word")
    print(f"Response from ChatGoogleGenerativeAI: {response_gemini}")

    print("Setup complete!")




if __name__ == "__main__":
    main()
