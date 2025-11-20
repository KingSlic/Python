from flask import Flask
from queries import get_students_list, get_student, get_students_with_teachers_list, get_student_by_name, remove_student

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


@app.route("/students_with_teachers")
def get_students_with_teachers():
    return get_students_with_teachers_list()



# Create a route that would fetch student by Name

@app.route("/students/<string:name>")
def student_by_name(name):
    student = get_student_by_name(name)
    
    if not student:
        return {"error": "Student not found"}, 404

    return student

# Create a route that would delete student by ID.
# Return message "Student successfully deleted" upon success and "Student ID not found" on failure (non-existent student ID)

@app.route("/students/delete/<int:studentId>", methods=["DELETE", "GET"])

def delete_student(studentId):
    return remove_student(studentId)
    

    


# Create your own route using a JOIN query with a filter condition
# For example, display students and their teachers where the teacher's name matches a given value.
# The route should accept a parameter (e.g., /students_with_teacher/<teacher_name>) and return the filtered results as JSON.