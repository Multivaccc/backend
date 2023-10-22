from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from llama_index import Document
from uuid import uuid4
from multivac import DB_DIR
from multivac.db import Book
from PyPDF2 import PdfReader


def _vectorize(book):
    folder = book.get_folder()
    documents = SimpleDirectoryReader(input_files=[f"{folder}/__raw__.pdf"]).load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    index.storage_context.persist(f"{folder}/index")
    return index

def process_pdf(book):
    return _vectorize(book)

def process_states(states):
    states = states.split("\n\n")[1:][0]
    li_states = states.split("\n")
    li_states = [[",".join(st.split(",")[0:-2]), st.split(",")[-2], st.split(",")[-1]] for st in li_states]
    return li_states

def parse_pdf(book):
    reader = PdfReader(f"{book.get_folder()}/__raw__.pdf")
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def _initialize_book(name, author):
    uuid = uuid4()
    book = Book(uuid, name, author, write=True)
    book.init_metadata()
    return book

def process_book(name, author):
    book = _initialize_book(name, author)
    return book

def _add_to_log(book, log, chat):
    log.append(chat)
    book.write_chat(log)
    return log

def _add_to_index(book, index, chat):
    folder = book.get_folder()
    doc_chat = Document(text=f"{chat['content']}\n\nFrom: {chat['type']}")
    if index:
        index.insert(document=doc_chat)
    else:
        index = GPTVectorStoreIndex.from_documents(documents=[doc_chat])
        index.storage_context.persist(f"{folder}/chat")
    return index

def update_chat(book, log, index, chat):
    log = _add_to_log(book, log, chat)
    index = _add_to_index(book, index, chat)
    return log, index

def process_chat(book, chat):
    log, index = book.get_chat()
    return update_chat(book, log, index, chat)
