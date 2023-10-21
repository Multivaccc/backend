from flask import Blueprint, request, jsonify
from http import HTTPStatus
from multivac.lib.process import process_book

book = Blueprint("book", __name__, url_prefix="/book")

@book.route("/all/", methods=["GET"])
def read_books():
    return {}

@book.route("/<uuid>", methods=["GET"])
def read_book(uuid):
    return {}

@book.route("/", methods=["POST"])
def create_book():
    name = request.json["name"]
    author = request.json["author"]
    pdf = request.files["file"]
    if not pdf.endswith(".pdf"):
        return {
            "message": "Invalid file format recieved.",
            "status": HTTPStatus.BAD_REQUEST
        }, HTTPStatus.BAD_REQUEST
    book = process_book(name, author, pdf)
    return {
        "book": book,
        "status": HTTPStatus.OK
    }, HTTPStatus.OK

@book.route("/<uuid>", methods=["PUT"])
def update_book(uuid):
    return {}

@book.route("/<uuid>", methods=["DELETE"])
def delete_book(uuid):
    return {}