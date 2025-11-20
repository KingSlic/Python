from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>This is home page</h1>"

@app.route("/students")
def get_students():
    students_list = get_students_list()
    return students_list






