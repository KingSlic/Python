import sqlite3

# Helper function for creating database connections
def get_db_connection():
    db_connection = sqlite3.connect("my_db.db")
    db_connection.row_factory = sqlite3.Row
    return db_connection


def get_students_list():
    db = get_db_connection()
    students = db.execute("SELECT * FROM students").fetchall()
    db.close()

    students_list = [dict(row) for row in students]
    return students_list

def get_student(studentId):
    db = get_db_connection()
    # student = [Row{"id": 1, "name": "John"}] | None
    student = db.execute("SELECT * FROM students WHERE id=?", (studentId,)).fetchone()
    if not student:
        return None
    
    return dict(student)


def get_students_with_teachers_list():
    db = get_db_connection()
    students_with_teachers = db.execute("SELECT students.id, students.name, students.grade, teachers.name AS teacher_name FROM students JOIN teachers ON students.teacher_id=teachers.id").fetchall()

    students_with_teachers_list = [dict(row) for row in students_with_teachers]
    return students_with_teachers_list


def get_student_by_name(studentName):
    db = get_db_connection()
    student = db.execute("SELECT * FROM students WHERE name=?", (studentName,)).fetchone()
    db.close()
    if student:
        return dict(student)
    
    return None


def delete_student_by_id(studentId):
    db = get_db_connection()
    student = db.execute("SELECT * FROM students WHERE id=?", (studentId,)).fetchone()

    if not student:
        db.close()
        return False
    
    db.execute("DELETE FROM students WHERE id=?", (studentId,))
    db.commit()
    db.close()

    return True

def get_students_by_teacher_name(teacher_name):
    db = get_db_connection()
    students = db.execute("SELECT students.id, students.name, students.grade, teachers.name AS teacher_name FROM students JOIN teachers ON students.teacher_id=teachers.id WHERE teachers.name=?", (teacher_name,)).fetchall()
    db.close()

    # students_list = [dict(row) for row in students]
    students_list = []
    for row in students:
        students_list.append(dict(row))

    return students_list

def create_student(name, age, grade, teacher_id):
    db = get_db_connection()
    result = db.execute("INSERT INTO students (name, age, grade, teacher_id) VALUES (?, ?, ?, ?)", (name, age, grade, teacher_id))
    studentId = result.lastrowid
    db.commit()
    newly_created_student = get_student(studentId)
    db.close()

    return newly_created_student


def update_student_by_id(studentId, data):
    db = get_db_connection()
    student = get_student(studentId)
    
    studentName = student["name"]
    if "name" in data:
        studentName = data["name"]

    studentAge = student["age"]
    if "age" in data:
        studentAge = data["age"]

    studentGrade = student["grade"]
    if "grade" in data:
        studentGrade = data["grade"]

    teacherId = student["teacher_id"]
    if "teacher_id" in data:
        teacherId = data["teacher_id"]

    db.execute("UPDATE students SET name=?, age=?, grade=?, teacher_id=? WHERE id=?", (studentName, studentAge, studentGrade, teacherId, studentId))
    db.commit()
    db.close()
    return True