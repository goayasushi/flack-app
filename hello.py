from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/japan/<city>")
def hello_world(city):
    return render_template("hello.html",city = city)