from langchain.schema import (
    SystemMessage,
    AIMessage,
    HumanMessage
)
from langchain.llms import OpenAIChat
from langchain.agents import initialize_agent
from llama_index.langchain_helpers.memory_wrapper import GPTIndexChatMemory
from multivac.lib.model import CLAUDE, GPT
from multivac.lib.prompt import (
    SYSTEM_TEMPLATE,
    SETTING_DESCRIPTION_TEMPLATE,
    STATE_EXTRACTION_TEMPLATE,
    IMAGE_PROMPT_GENERATION_TEMPLATE
)
from multivac.lib.process import parse_pdf
import replicate
from textwrap import dedent


def generate_image_prompt(prompt):
    messages = [HumanMessage (
                content=f'''
                    ```text
                    {prompt}
                    ```
                    {IMAGE_PROMPT_GENERATION_TEMPLATE}
                ''')]
    response = GPT.predict_messages(messages)
    return response.content

def generate_image(prompt, width=512, height=512):
    model = "doriandarko/sdxl-hiroshinagai:563a66acc0b39e5308e8372bed42504731b7fec3bc21f2fcbea413398690f3ec"
    input = {
        "prompt": prompt,
        "width": width,
        "height": height,
    }
    output = replicate.run(model,input=input)
    url = output[0]
    return url

def timeline(book):
    text = parse_pdf(book)
    messages = [
        HumanMessage(
            content=f'''
            ```
            {text}
            ```
            {STATE_EXTRACTION_TEMPLATE}'''
        )
    ]
    response = CLAUDE.predict_messages(messages)
    return {
        "content": response.content,
        "type": "agent"
    }

def setting(index, book):
    # query_engine = index.as_query_engine()
    # response = query_engine.query("what is the main beginning event, scene or setting of the text? include as much detail and description as possible about the characters, location and plot.")
    # print(response)
    text = parse_pdf(book)
    messages = [
        HumanMessage(
            content=f'''
                ```context
                {text}
                ```
                {SETTING_DESCRIPTION_TEMPLATE}
            '''
        )
    ]
    response = CLAUDE.predict_messages(messages)
    return response.content.split("\n\n")[-1]

def chat(chat_index, book_index, action, states, timestamp):
    book_query = book_index.as_query_engine()
    chat_query = chat_index.as_query_engine()
    print(action)
    book_response = book_query.query(action["content"])
    book_response = book_response.response
    chat_response = chat_query.query(action["content"])
    chat_response = chat_response.response
    prompt = dedent(f'''\
        ```states
        {states}
        ```
        ```story
        {book_response}
        ```
        ```chat
        {chat_response}
        ```
        ```timestamp
        {timestamp}
        ```
        ```action
        {action}
        ```
    ''')
    messages = [
        SystemMessage(
            content=SYSTEM_TEMPLATE
        ),
        AIMessage(
            content="Done."
        ),
        HumanMessage(
            content=prompt
        )
    ]
    response = GPT.predict_messages(messages)
    return {
        "content": response.content,
        "type": "agent",
        "imageURL": ""
    }
    