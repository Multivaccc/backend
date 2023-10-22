from datetime import datetime
from multivac.db import Book
from .generate import setting
from .process import process_chat
from .prompt import SETTING_DESCRIPTION_TEMPLATE

def extract_states():
    pass

def init_setting(book):
    _, index = book.get_chat()
    initial_setting = setting(index)
    di_setting = {
        "content": initial_setting,
        "type": "agent"
    }
    log, _ = process_chat(book, di_setting)
    return log
