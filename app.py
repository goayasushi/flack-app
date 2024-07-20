from flask import Flask
from flask import render_template

app = Flask(__name__)

bullets = [
    "箇条書き1",
    "箇条書き2",
    "箇条書き3",
    "箇条書き4",
    "箇条書き5",
    "箇条書き6",
]

@app.route("/")
def index():
    return render_template("index.html")