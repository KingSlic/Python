from flask import Flask, jsonify, request
from queries import get_students_list, get_student, get_student_by_name,delete_student_by_id, create_student, update_student_by_id

app = Flask(__name__)

@app.route("/")
def main_route():
    return "<h1>This is main route - Updated</h1>"

@app.route("/students")
def get_students():
    students_list = get_students_list()
    return students_list

@app.route("/students/<int:studentId>")
def get_student_details(studentId):
    student = get_student(studentId)
    if student is None:
        return {"error": "student not found"}, 404

    return student


# @app.route("/students_with_teachers")
# def get_students_with_teachers():
#     return get_students_with_teachers_list()



# Create a route that would fetch student by Name
@app.route("/students/<string:studentName>")
def get_student_name_route(studentName):
    student = get_student_by_name(studentName)
    if not student:
        return {"error": "student with this name was not found."}, 404
    
    return student



# Create a route that would delete student by ID.
# Return message "Student successfully deleted" upon success and "Student ID not found" on failure (non-existent student ID)
@app.get("/students/delete/<int:studentId>")
def delete_student_route(studentId):
    is_deleted = delete_student_by_id(studentId)
    if not is_deleted:
        return jsonify({"error": "Failed to delete student"})
    
    return jsonify({"message": "Student successfully deleted"})



# Create your own route that uses a JOIN query with a filter condition.
# For example, display students and their teachers where the teacher's name matches a given value.
# The route should accept a parameter (e.g., /students_with_teacher/<teacher_name>) and return the filtered results as JSON.
# @app.route("/students_with_teacher/<teacher_name>")
# def teachers_students(teacher_name):
#     return get_students_by_teacher_name(teacher_name)


@app.route('/students', methods=['POST'])
def create_student_route():
    data = request.get_json()

    if "teacher_id" not in data:
        return jsonify({"error": "Please provide the teacher ID"})
    
    if "name" not in data:
        return jsonify({"error": "Please provide the student name"})
    
    if "age" not in data:
        return jsonify({"error": "Please provide the student age"})
    
    if "grade" not in data:
        return jsonify({"error": "Please provide the student grade"})

    student_name = data["name"]
    student_age = data["age"]
    student_grade = data["grade"]
    teacher_id = data["teacher_id"]


    student_dict = create_student(student_name, student_age, student_grade, teacher_id)
    if student_dict:
        return jsonify({"message": "Student successfully created.", "student": student_dict}), 201
    
    return {"error": "Failed to create student"}


@app.route("/students/<int:studentId>", methods=['PUT'])
def update_student_route(studentId):
    data = request.get_json()
    is_updated = update_student_by_id(studentId, data)
    if is_updated:
        return jsonify({"message": "Student successfully updated!"})
      
    return jsonify({"error": "Failed to update student"})

@app.route("/students/<int:studentId>", methods=['DELETE'])
def delete_student_route2(studentId):
    is_deleted = delete_student_by_id(studentId)
    if not is_deleted:
        return jsonify({"error": "Failed to delete student"})
    
    return jsonify({"message": "Student deleted successfully!"})

# This is what we sent v
# {
#     "name": "John",
#     "grade": "A",
#     "age": 19
# }
# # this is what we recieved from the API
# {
#     "data_received": {
#         "age": 19,
#         "grade": "A",
#         "name": "John"
#     }
# }

