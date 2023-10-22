# from langchain.llms.openai import OpenAIChat
from langchain.llms.anthropic import Anthropic
from ..config import OPENAI_API_KEY, ANTHROPIC_API_KEY

# GPT = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4")
CLAUDE = Anthropic(anthropic_api_key=ANTHROPIC_API_KEY, max_tokens=2048)