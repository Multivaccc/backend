import os
from flask import Flask, render_template, request, send_file, jsonify

app = Flask(__name__)

# if __name__ == "__main__":
#     app.run(debug=True)