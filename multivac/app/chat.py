from flask import Blueprint, request, jsonify
from http import HTTPStatus
import os
from multivac.db import Book
from multivac.lib.process import process_chat

chat = Blueprint("chat", __name__, url_prefix="/book")

@chat.route("/<uuid>/chat/", methods=["GET"])
def read_chat(uuid):
    book = Book.query(uuid)
    if not book:
        return {
            "message": "Book does not exist.",
            "status": HTTPStatus.NOT_FOUND
        }, HTTPStatus.NOT_FOUND
    book = Book(**book)
    log, _ = book.get_chat()
    return {
        "log": log,
        "status": HTTPStatus.OK
    }, HTTPStatus.OK

@chat.route("/<uuid>/chat/", methods=["POST"])
def create_chat(uuid):
    chat = request.json["chat"]
    if not chat:
        return {
            "message": "Invalid chat.",
            "status": HTTPStatus.BAD_REQUEST
        }, HTTPStatus.BAD_REQUEST
    book = Book.query(uuid)
    if not book:
        return {
            "message": "Book does not exist.",
            "status": HTTPStatus.NOT_FOUND
        }, HTTPStatus.NOT_FOUND
    book = Book(**book)
    log, index = process_chat(book, chat)
    return {
        "log": log,
        "status": HTTPStatus.OK
    }, HTTPStatus.OK