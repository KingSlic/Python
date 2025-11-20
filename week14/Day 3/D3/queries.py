import os, sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "my_db.db")


# Helper function for creating database connections
def get_db_connection():
    db_connection = sqlite3.connect(DB_PATH)
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
    student = db.execute("SELECT * FROM students WHERE id=?", (studentId,)).fetchone()
    db.close()
    
    if not student:
        return None
    
    return dict(student)

def get_student_by_name(name):
    db = get_db_connection()
    student_name = db.execute("SELECT * FROM students WHERE name = ? COLLATE NOCASE", (name,)).fetchone()
    db.close()
    
    if not student_name:
        return False
    
    return dict(student_name)


def get_students_with_teachers_list():
    db = get_db_connection()
    students_with_teachers = db.execute("SELECT students.id, students.name, students.grade, teachers.name AS teacher_name FROM students JOIN teachers ON students.teacher_id=teachers.id").fetchall()
    db.close()
    
    students_with_teachers_list = [dict(row) for row in students_with_teachers]
    return students_with_teachers_list


def remove_student(studentId):
    db = get_db_connection()
    removed_student = db.execute("SELECT * FROM students WHERE id=?", (studentId,)).fetchone()
    
    if not removed_student:
        db.close()
        return {"error": f"Student with ID {studentId} not found"}, 404
    
    db.execute("DELETE FROM students WHERE id=?", (studentId,))
    db.commit()
    db.close()
    
    return {
        "message": f"Student with ID {studentId} has been deleted successfully",
        "deleted_student": dict(removed_student)
    }