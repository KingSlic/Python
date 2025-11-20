import sqlite3

db_connection = sqlite3.connect("my_db.db")

teacher_table_query = """
    CREATE TABLE teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
"""
db_connection.execute(teacher_table_query)
db_connection.commit()

teacher_query = "INSERT INTO teachers (name) VALUES (?)"
db_connection.execute(teacher_query, ("Teacher 1",))
db_connection.commit()



studentsTable = """
    CREATE TABLE students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade INTEGER NOT NULL,
        teacher_id INTEGER NOT NULL
    )
"""

db_connection.execute(studentsTable)
db_connection.commit()

students_records_query = """
    INSERT INTO students (name, age, grade, teacher_id) VALUES (?, ?, ?, ?)
"""

session = SessionLocal()
student = Student(name="John", age=20, grade="A", teacher_id=1)
session.add(student)
session.flush()

db_connection.executemany(students_records_query, [
    ("Alice", 20, "A", 1),
    ("Bob", 22, "B", 1),
    ("Charlie", 19, "A", 1),
])

db_connection.commit()

print("Database and tables created successfully")
# """
# INSERT INTO students 
#     (name, age, grade) 
# VALUES 
#     ("Alice", 20, "A"),
#     ("Bob", 22, "B"),
#     ("Charlie", 19, "A")
# """