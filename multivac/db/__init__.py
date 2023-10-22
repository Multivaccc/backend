from llama_index import StorageContext, load_index_from_storage
from llama_index.vector_stores import SimpleVectorStore
from llama_index.storage.docstore import SimpleDocumentStore
from llama_index.storage.index_store import SimpleIndexStore
import os
import json
from multivac import DB_DIR

BOOK_DIR = f"{DB_DIR}/book"

class Book():
    
    def __init__(self, uuid, name, author, write=False):
        self.uuid = uuid
        self.name = name or ""
        self.author = author or ""
        if write:
            os.makedirs(f"{BOOK_DIR}/{self.uuid}")
            os.makedirs(f"{BOOK_DIR}/{self.uuid}/chat")
            json.dump([], open(f"{BOOK_DIR}/{self.uuid}/log.json", "w+"))

    @classmethod
    def all(cls):
        books = []
        uuids = os.listdir(BOOK_DIR)
        for uuid in uuids:
            books.append(json.load(open(f"{BOOK_DIR}/{uuid}/metadata.json", "r")))
        return books

    @classmethod
    def query(cls, uuid):
        try:
            book = json.load(open(f"{BOOK_DIR}/{uuid}/metadata.json", "r"))
            return book
        except FileNotFoundError as e:
            return ""

    def get_folder(self):
        return f"{BOOK_DIR}/{self.uuid}"

    def get_chat(self):
        folder = self.get_folder()
        persist_dir = f"{folder}/chat"
        chat = json.load(open(f"{folder}/log.json", "r+"))
        index = None
        if os.listdir(persist_dir):
            index = load_index_from_storage(storage_context=StorageContext.from_defaults(
                docstore=SimpleDocumentStore.from_persist_dir(persist_dir=persist_dir),
                vector_store=SimpleVectorStore.from_persist_dir(persist_dir=persist_dir),
                index_store=SimpleIndexStore.from_persist_dir(persist_dir=persist_dir)
            ))
        return chat, index

    def write_chat(self, log):
        folder = self.get_folder()
        json.dump(log, open(f"{folder}/log.json", "w+"))

    def init_metadata(self):
        f = open(f"{self.get_folder()}/metadata.json", "w")
        json.dump({
            "uuid": str(self.uuid),
            "name": self.name,
            "author": self.author
        }, f)
        f.close()

    def json(self):
        return {
            "uuid": self.uuid,
            "name": self.name,
            "author": self.author
        }