import sqlite3
from sqlalchemy import create_engine, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column, relationship

engine = create_engine("sqlite:///my_db.db", echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Teacher(Base):
    __tablename__ = "teachers"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False)

    # One-to-many: a teacher has many students
    students: Mapped[list["Student"]] = relationship("Student", back_populates="teacher")


class Student(Base):
    __tablename__ = "students"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False)
    age = mapped_column(Integer, nullable=False)
    grade = mapped_column(Integer, nullable=False)

    teacher_id = mapped_column(ForeignKey("teachers.id"), nullable=False)

    # Reference back to teacher
    teacher: Mapped[int] = relationship("Teacher", back_populates="students")

    # a helper method to convert student object to dictionary
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "grade": self.grade,
            "teacher_id": self.teacher_id
        }

Base.metadata.create_all(engine)


def get_students_list():
    session = SessionLocal()
    students = session.query(Student).all()

    students_list = [row.to_dict() for row in students]
    return students_list

def get_student(studentId):
    session = SessionLocal()
    student = session.query(Student).filter_by(id=studentId).get()
    if not student:
        return None
    
    return student.to_dict()


# def get_students_with_teachers_list():
#     db = get_db_connection()
#     students_with_teachers = db.execute("SELECT students.id, students.name, students.grade, teachers.name AS teacher_name FROM students JOIN teachers ON students.teacher_id=teachers.id").fetchall()

#     students_with_teachers_list = [dict(row) for row in students_with_teachers]
#     return students_with_teachers_list


def get_student_by_name(studentName):
    session = SessionLocal()
    student = session.query(Student).filter_by(name=studentName).get()
    if student:
        return student.to_dict()
    
    return None


def delete_student_by_id(studentId):
    session = SessionLocal()
    student = session.query(Student).filter_by(id=studentId).get()

    if not student:
        return False
    
    session.delete(student)
    session.commit()
    return True

# def get_students_by_teacher_name(teacher_name):
#     db = get_db_connection()
#     students = db.execute("SELECT students.id, students.name, students.grade, teachers.name AS teacher_name FROM students JOIN teachers ON students.teacher_id=teachers.id WHERE teachers.name=?", (teacher_name,)).fetchall()
#     db.close()

#     # students_list = [dict(row) for row in students]
#     students_list = []
#     for row in students:
#         students_list.append(dict(row))

#     return students_list

def create_student(name, age, grade, teacher_id):

    session = SessionLocal()
    # Student(name=name, age=age, grade=grade, teacher_id=teacher_id)
    student = Student()
    student.name = name
    student.age = age
    student.grade = grade
    student.teacher_id = teacher_id

    session.add(student)
    session.commit()
    
    session.refresh(student)

    return student


def update_student_by_id(studentId, data):
    session = SessionLocal()
    student = get_student(studentId)
    if not student:
        return False

    studentName = data.get("name", student.get("name"))
    studentAge = data.get("age", student.get("age"))
    studentGrade = data.get("grade", student.get("grade"))
    teacherId = data.get("teacher_id", student.get("teacher_id"))

    student.name = studentName
    student.age = studentAge
    student.grade = studentGrade
    student.teacher_id = teacherId

    session.commit()
    
    return True