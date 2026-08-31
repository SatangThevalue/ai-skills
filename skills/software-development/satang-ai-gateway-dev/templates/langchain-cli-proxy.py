from langchain_openai import ChatOpenAI

# Connects LangChain to the local Hermes CLI Proxy API
# Used for fast, low-cost local processing via proxy models (e.g., gemini-3.1-pro-low)
llm = ChatOpenAI(
    base_url="http://localhost:42869/v1",
    api_key="dummy_key_cli_proxy", 
    model="gemini-3.1-pro-low",
    temperature=0.0
)