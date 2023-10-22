from langchain.chat_models import ChatOpenAI, ChatAnthropic
from ..config import OPENAI_API_KEY, ANTHROPIC_API_KEY

# GPT = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4")
CLAUDE = ChatAnthropic(anthropic_api_key=ANTHROPIC_API_KEY, max_tokens=2048)