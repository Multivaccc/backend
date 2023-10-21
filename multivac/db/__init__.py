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

    def get_folder(self):
        return f"{BOOK_DIR}/{self.uuid}"

    def init_metadata(self):
        f = open(f"{self.get_folder()}/metadata.json", "w")
        json.dump({
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