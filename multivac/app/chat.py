from flask import Blueprint, request, jsonify
from http import HTTPStatus
import os
from multivac.db import Book
from multivac.lib.process import process_chat
from multivac.lib.pipeline import init_setting, run_action, get_image

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
    str_chat = request.json.get("chat", None)
    book = Book.query(uuid)
    if not book:
        return {
            "message": "Book does not exist.",
            "status": HTTPStatus.NOT_FOUND
        }, HTTPStatus.NOT_FOUND
    book = Book(**book)
    log, _ = book.get_chat()
    url = None
    if not str_chat and log:
        return {
            "message": "Invalid chat.",
            "status": HTTPStatus.BAD_REQUEST
        }, HTTPStatus.BAD_REQUEST
    if not str_chat:
        process_chat(book, {
            "content": "_",
            "type": "_",
            "imageURL": ""
        })
        log, _ = init_setting(book)
    else:
        log, chat_index = process_chat(book, str_chat)
        book_index = book.get_index()
        log, _, nt = run_action(chat_index, book_index, book, log, str_chat)
        url = ""
        # if (nt%2 == 0):
        #     url = get_image(log[-1])
        #     print(url)
        log[-1] = { "content": log[-1]['content'],"type": log[-1]['type'], "imageURL": url}
    return {
        "log": log,
        "status": HTTPStatus.OK
    }, HTTPStatus.OK