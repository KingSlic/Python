from flask import Flask, request
from jose import jwt
import bcrypt
from models import Session, User, Note, Base, engine
from datetime import datetime, timedelta


SECRET_KEY = "a3ab6a9cd06bcbf48ac6857290d817dd40dca64404adfa3e9d2e09a568c90f6f"


Base.metadata.create_all(engine)
app = Flask(__name__)


# I'm using a helper function here instead of creating another route
def get_logged_in_user_id():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    token = auth_header.split(' ')[1]


    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        return int(user_id)
    except Exception as e:
        return None


@app.route("/register", methods=["POST"])
def create_user():
    data = request.get_json()
    session = Session()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name:
        return {"error": "invalid name"}
    
    if not email:
        return {"error": "invalid email"}
    
    if not password:
        return {"error": "invalid password"}
    
    existing_user = session.query(User).filter_by(email=email).first()

    if existing_user:
        return {"error": "email is already taken"}
    
    user = User(name=name, email=email, password="")
    user.set_password(password)
    session.add(user)
    session.commit()

    return user.to_dict()


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    session = Session()

    email = data.get("email")
    password = data.get("password")

    if not email:
        return {"error": "invalid email"}
    
    if not password:
        return {"error": "invalid password"}
    
    existing_user = session.query(User).filter_by(email=email).first()

    if not existing_user:
        return {"error": "invalid credentials"}
    
    if not existing_user.check_password(password):
        return {"error": "invalid credentials"}
    
    payload = {
        "sub": str(existing_user.id),
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return {"access_token": token, "user": existing_user.to_dict()}



@app.route("/me", methods=["GET"])
def get_current_user():
    
    user_id = get_logged_in_user_id()

    if not user_id:
        return {"error": "unauthorized"}
    
    #fetch user from db
    session = Session()
    user = session.query(User).get(user_id)

    if not user:
        return {"error": "user not found"}
    
    return user.to_dict()



@app.route("/notes", methods=["POST"])
def create_note():
    
    user_id = get_logged_in_user_id()

    if not user_id:
        return {"error": "unauthorized"}
    
    data = request.get_json()

    title = data.get("title")
    content = data.get("content")

    if not title:
        return {"error": "title is required"}
    
    if not content:
        return {"error": "content is required"}
    
    session = Session()
    note = Note(title=title, content=content, user_id=user_id)
    session.add(note)
    session.commit()

    return note.to_dict()



@app.route("/notes", methods=["GET"])
def get_notes():

    user_id = get_logged_in_user_id()
    
    if not user_id:
        return {"error": "unauthorized"}
    
    session = Session()
    #many-to-one connection
    notes = session.query(Note).filter_by(user_id=user_id).all()

    notes_list = [note.to_dict() for note in notes]
    return {"notes": notes_list}


@app.route("/notes/<int:note_id>", methods=["GET"])
def get_note_by_id(note_id):
    
    user_id = get_logged_in_user_id()
    if not user_id:
        return {"error": "unauthorized"}
    
    session = Session()
    note = session.query(Note).get(note_id)
    if not note:
        return {"error": "note not found"}
    
    if note.user_id != user_id:
        return {"error": "access denied"}
    
    return note.to_dict()


@app.route("/notes/<int:note_id>", methods=["PUT"])
def update_note(note_id):

    #Authorization
    user_id = get_logged_in_user_id()
    if not user_id:
        return {"error": "unauthorized"}
    
    #Load the actual note from the db
    session = Session()
    note = session.query(Note).get(note_id)

    if not note:
        return {"error": "note not found"}
    
    #make sure you're not updating someone else's note
    if note.user_id != user_id:
        return {"error": "access denied"}
    
    # ___________ -------- ____________

    # Time to update the note
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")

    if not title:
        return {"error": "title is required"}
    
    if not content:
        return {"error": "content is required"}
    
    note.title = title
    note.content = content
    
    session.commit()

    return note.to_dict()



@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):

    user_id = get_logged_in_user_id()
    if not user_id:
        return {"error": "unauthorized"}
    
    session = Session()
    note = session.query(Note).get(note_id)

    if not note:
        return {"error": "note not found"}
    
    if note.user_id != user_id:
        return {"error": "access denied"}
    

    session.delete(note)
    session.commit()

    return {"message": "note deleted successfully"}