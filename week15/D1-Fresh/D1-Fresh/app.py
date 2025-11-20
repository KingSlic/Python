from flask import Flask, request
from models import Session, Base, engine, User

# This line will create all tables based on classes defined in models.py
Base.metadata.create_all(engine)

app = Flask(__name__)

@app.route("/")
def main_route():
    return "Hello World"


@app.route("/users")
def get_users_route():
    session = Session()
    users = session.query(User).all()
    users_list = [row.to_dict() for row in users]
    return users_list

@app.route("/users/<int:userId>")
def fetch_user_by_id(userId):
    session = Session()
    user = session.query(User).filter_by(id=userId).first()
    if not user:
        return {"error": "User not found"}
    
    return user.to_dict()

@app.route("/users", methods=["POST"])
def create_user_route():
    data = request.get_json()

    session = Session()
    user = User()
    user.name = data["name"]
    user.email = data["email"]
    user.password = data["password"]
    # Add the user object to the database (NOT SAVED YET)
    session.add(user)

    # SAVE ALL CHANGES TO DATABASE
    session.commit()

    return user.to_dict()


@app.route("/users/<int:userId>", methods=["PUT"])
def update_user_route(userId):
    data = request.get_json()
    session = Session()

    user = session.query(User).filter_by(id=userId).first()
    # If user not found in database, nothing to update, return an error
    if not user:
        return {"error": "User not found"}
    
    user.name = data["name"]
    user.email = data["email"]
    user.password = data["password"]
    # SAVE ALL CHANGES TO DATABASE
    session.commit()

    return user.to_dict()

@app.route("/users/<int:userId>", methods=["DELETE"])
def delete_user_by_id(userId):
    session = Session()
    user = session.query(User).filter_by(id=userId).first()
    if not user:
        return {"error": "User not found"}
    
    session.delete(user)
    session.commit()
    return user.to_dict()