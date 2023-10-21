from flask import Blueprint, request, jsonify
from http import HTTPStatus
import os
from multivac.db import Book, Chat

chat = Blueprint("chat", __name__, url_prefix="/book")

@chat.route("/<uuid>/chat", methods=["GET"])
def read_chat(uuid):
    book = Book.query(uuid)
    if not book:
        return {
            "message": "Book does not exist.",
            "status": HTTPStatus.NOT_FOUND
        }, HTTPStatus.NOT_FOUND
    book.get_chat()

@chat.route("/<uuid>/chat", methods=["POST"])
def create_chat():
    pass