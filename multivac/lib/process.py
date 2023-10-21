from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from uuid import uuid4
from multivac import DB_DIR
from multivac.db import Book

def _vectorize(book):
    folder = book.get_folder()
    documents = SimpleDirectoryReader(input_files=[f"{folder}/__raw__.pdf"]).load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    index.storage_context.persist(f"{folder}/index")
    return index

def process_pdf(book):
    return _vectorize(book)

def _initialize_book(name, author):
    uuid = uuid4()
    book = Book(uuid, name, author)
    book.init_metadata()
    return book

def process_book(name, author):
    book = _initialize_book(name, author)
    return book