from flask import Blueprint, request, jsonify
from http import HTTPStatus
import os
from multivac.lib.process import process_book, process_pdf

book = Blueprint("book", __name__, url_prefix="/book")

@book.route("/all/", methods=["GET"])
def read_books():
    return {}

@book.route("/<uuid>", methods=["GET"])
def read_book(uuid):
    return {}

@book.route("/", methods=["POST"])
def create_book():
    name = request.form.get("name", None)
    author = request.form.get("author", None)
    pdf = request.files.get("file", None)
    if pdf is None:
        return {
            "message": "No file provided.",
            "status": HTTPStatus.BAD_REQUEST
        }, HTTPStatus.BAD_REQUEST
    _, file_extension = os.path.splitext(pdf.filename)
    if file_extension.lower() != ".pdf":
        return {
            "message": "Invalid file format received. Please upload a PDF file.",
            "status": HTTPStatus.BAD_REQUEST
        }, HTTPStatus.BAD_REQUEST
    book = process_book(name, author)
    folder = book.get_folder()
    pdf.save(f"{folder}/__raw__.pdf")
    _ = process_pdf(book)
    return {
        "book": book.json(),
        "status": HTTPStatus.OK
    }, HTTPStatus.OK


@book.route("/<uuid>", methods=["PUT"])
def update_book(uuid):
    return {}

@book.route("/<uuid>", methods=["DELETE"])
def delete_book(uuid):
    return {}