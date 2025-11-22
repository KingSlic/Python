from flask import Flask, request
from models import Session, Base, engine, User, Post
import bcrypt
from datetime import datetime, timedelta, timezone

from jose import jwt

SECRET_KEY = "b2dc9512a093a3188dc92f6897326b95"

# This line will create all tables based on classes defined in models.py
Base.metadata.create_all(engine)

app = Flask(__name__)

@app.route("/")
def main_route():
    return "Hello World2"


@app.route("/users")
def get_users_route():
    # Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjM2MDE5MjMsImlhdCI6MTc2MzYwMDEyMywic3ViIjoyLCJpbnN0cnVjdG9yIjoiQWhtZWQifQ.j2_IFuFLkg4tJI5VfsOycm1uyRm6gyng_qGpMPTWetk
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return {"error": "Please provide the JWT token"}

    # ["Bearer", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"]
    token_without_bearer = auth_header.split(' ')[1]
    print("auth_header:", auth_header)
    
    try:
        decoded_token = jwt.decode(token_without_bearer, SECRET_KEY, algorithms=["HS256"])
        print("---------------- Decoded Token -----------------")
        print(decoded_token)
        print("-------------------- End of decoded token ----------------")

        session = Session()
        users = session.query(User).all()
        users_list = [row.to_dict() for row in users]
        return users_list
    except Exception as e:
        return {"error": "Failed to decode the token, please login first!"}


@app.route("/users/<int:userId>")
def fetch_user_by_id(userId):
    session = Session()
    user = session.query(User).filter_by(id=userId).first()
    if not user:
        return {"error": "User not found"}
    
    return user.to_dict()


@app.route("/users/<int:userId>/posts")
def get_user_posts(userId):
    session = Session()
    user = session.query(User).filter_by(id=userId).first()
    if not user:
        return {"error": "User is not found!"}, 404
    
    user_posts = []
    for post in user.posts:
        user_posts.append(post.to_dict())

    return user_posts

@app.route("/users", methods=["POST"])
def create_user_route():
    data = request.get_json()

    hashed_password = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt()).decode('utf-8')
    session = Session()
    user = User()
    user.name = data["name"]
    user.email = data["email"]
    user.password = hashed_password
    # Add the user object to the database (NOT SAVED YET)
    session.add(user)

    # SAVE ALL CHANGES TO DATABASE
    session.commit()

    return user.to_dict()



@app.route("/login", methods=["POST"])
def login_route():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    session = Session()
    user = session.query(User).filter_by(email=email).first()
    if not user:
        return {"error": "1st - invalid credentials!"}
    
    # 123 => fdVkhVetUSdS8W3v2VL0y
    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
            "iat": datetime.now(timezone.utc),
            "sub": str(user.id),
            "instructor": "Ahmed"
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return {
            "message": "succesful login!",
            "type": "Bearer",
            "token": token
        }
    else:
        return {"error": "2nd - invalid credentials!"}



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


# Posts CRUD
@app.route("/posts")
def get_all_posts():
    session = Session()
    posts = session.query(Post).all()
    all_posts = [post.to_dict() for post in posts]
    return all_posts

@app.route("/posts", methods=["POST"])
def create_post_route():
    data = request.get_json()
    data["name"]
    data.get("name")

    session = Session()
    user_id = data["user_id"]
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        return {"error": "User does not exist!"}
    
    post = Post(title=data["title"], content=data["content"], user_id=data["user_id"])
    session.add(post)
    session.commit()

    return post.to_dict()

@app.route("/posts/<int:postId>", methods=["PUT"])
def update_post_route(postId):
    session = Session()
    post = session.query(Post).filter_by(id=postId).first()
    if not post:
        return {"error": "post not found!"}, 404
    
    data = request.get_json()
    post.title = data["title"]
    post.content = data["content"]
    post.user_id = data["user_id"]

    session.commit()
    
    return {
        "post": post.to_dict(),
        "user": post.creator.to_dict()
    }