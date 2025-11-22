from flask import Flask, request
from models import Session, Base, engine, User, Note
import bcrypt
from jose import jwt



Base.metadata.create_all(engine)

app = Flask(__name__)


@app.route("/register", methods=["POST"])
def create_user():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return {"error": "Please provide the JWT token"}