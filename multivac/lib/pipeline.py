from datetime import datetime
from multivac.db import Book
from multivac.lib.generate import setting, timeline, chat, generate_image, generate_image_prompt
from multivac.lib.process import process_chat, process_states, update_chat

def extract_states(book):
    states = timeline(book)
    states["content"] = process_states(states["content"])
    with open(f"{book.get_folder()}/states.tsv", "w+") as f:
        for state in states["content"]:
            f.write("\t".join(state))
    return states

def init_setting(book):
    index = book.get_index()
    initial_setting = setting(index, book)
    di_setting = {
        "content": initial_setting,
        "type": "agent",
        "imageURL": ""
    }
    log, index = process_chat(book, di_setting)
    return log, index

def run_action(chat_index, book_index, book, log, action):
    ot = book.get_timestamp()
    states = book.get_states()
    message = chat(chat_index, book_index, action, states, ot)
    log, index = update_chat(book, log, chat_index, message)
    nt = book.increment()
    return log, index, nt

def get_image(response):
    prompt = generate_image_prompt(response)
    url = generate_image(prompt)
    return url