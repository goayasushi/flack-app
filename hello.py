from flask import Flask

app = Flask(__name__)

@app.route("/japan/<city>")
def hello_city(city):
    return f"Hello, {city} in Japan!"