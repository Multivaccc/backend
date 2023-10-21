import os
from flask import Flask, render_template, request, send_file, jsonify
from multivac.app.book import book

app = Flask(__name__)
app.register_blueprint(book)

if __name__ == "__main__":
    app.run(port=8000, debug=True)