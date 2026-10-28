from flask import Flask, send_file
import os

app = Flask(__name__)

@app.route("/")
def index():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    return send_file(html_path, mimetype="text/html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
