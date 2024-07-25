from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager

from datetime import datetime
import pytz
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.urandom(24)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(pytz.timezone("Asia/Tokyo")))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(12))

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        posts = Post.query.order_by(Post.created_at.desc()).all()
        return render_template("index.html", posts = posts)

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")

        post = Post(title=title, body=body)

        db.session.add(post)
        db.session.commit()
        return redirect("/")
    else:
        return render_template("create.html")
    
@app.route("/<int:id>/update", methods=["GET", "POST"])
def update(id):
    post = Post.query.get(id)
    if request.method == "GET":
        return render_template("update.html", post=post)
    else:
        post.title = request.form.get("title")
        post.body = request.form.get("body")

        db.session.commit()
        return redirect("/")
    
@app.route("/<int:id>/delete", methods=["GET"])
def delete(id):
    post = Post.query.get(id)
    
    db.session.delete(post)
    db.session.commit()
    return redirect("/")