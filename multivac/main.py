import os
from flask import Flask, render_template, request, send_file, jsonify
from multivac.app import book, chat

app = Flask(__name__)
app.register_blueprint(book)
app.register_blueprint(chat)

if __name__ == "__main__":
    app.run(port=8000, debug=True)