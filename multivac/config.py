import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env"))

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
REPLICATE_API_KEY = os.environ.get('REPLICATE_API_KEY')