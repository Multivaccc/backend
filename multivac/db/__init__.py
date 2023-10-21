from multivac import DB_DIR
import os
import json

BOOK_DIR = f"{DB_DIR}/book"

class Book():
    
    def __init__(self, uuid, name, author):
        self.uuid = uuid
        self.name = name or ""
        self.author = author or ""
        os.makedirs(f"{BOOK_DIR}/{self.uuid}")

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