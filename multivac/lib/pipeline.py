from datetime import datetime
from .generate import setting
from multivac.db import Book

def extract_states():
    pass

def generate_settings(uuid):
    book = Book.query(uuid)
    if not book:
        return "Book does not exist"
    book = Book(**book)
    _, index = book.get_chat()
    settings = setting(index)
    return settings.settings