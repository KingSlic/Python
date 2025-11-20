import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "my_db.db")

db_connection = sqlite3.connect(DB_PATH)
db_connection.row_factory = sqlite3.Row

db_connection.execute("DROP TABLE IF EXISTS students")
db_connection.execute("DROP TABLE IF EXISTS teachers")
db_connection.commit()

# Enforce foreign keys (good practice; prevents invalid teacher_id inserts)
db_connection.execute("PRAGMA foreign_keys = ON")


# --------------------------
# 1) CREATE TABLES
# --------------------------
db_connection.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
""")
db_connection.commit()

db_connection.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL,
        teacher_id INTEGER NOT NULL,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id)
    )
""")
db_connection.commit()

# --------------------------
# 2) SEED / UPDATE TEACHERS
# --------------------------
# Insert initial row (first run) then rename it
db_connection.execute("INSERT INTO teachers (name) VALUES (?)", ("Teacher 1",))
db_connection.commit()

db_connection.execute(
    "UPDATE teachers SET name = ? WHERE name = ?",
    ("George Washington", "Teacher 1")
)
db_connection.commit()

# IMPORTANT: single-element tuples MUST have a trailing comma
db_connection.executemany(
    "INSERT INTO teachers (name) VALUES (?)",
    [
        ("John Adams",),
        ("Thomas Jefferson",),
        ("James Madison",),   # <-- comma added
        ("James Monroe",),    # <-- comma added
        ("Andrew Jackson",),  # <-- comma added
    ]
)
db_connection.commit()

# --------------------------
# 3) SEED STUDENTS
# --------------------------
students_records_query = """
    INSERT INTO students (name, age, grade, teacher_id) VALUES (?, ?, ?, ?)
"""

# Teacher IDs now are:
# 1: George Washington, 2: John Adams, 3: Thomas Jefferson,
# 4: James Madison, 5: James Monroe, 6: Andrew Jackson
db_connection.executemany(students_records_query, [
    ("Alice", 20, "A", 1),
    ("Bob", 22, "B", 1),
    # ("Charlie", 19, "A", 1),  # you said you deleted Charlie; leave commented if desired
])
db_connection.commit()

db_connection.executemany(students_records_query, [
    ("Jacob", 22, "A", 3),
    ("Eve", 19, "C", 2),
    ("Frank", 21, "B", 4),
    ("Grace", 19, "A", 2),
    ("Hector", 22, "C", 3),
    ("Ivy", 20, "B", 6),
    ("Jack", 22, "A", 5),
    ("Kara", 21, "A", 5),
    ("Liam", 23, "B", 4),
    ("Mona", 18, "A", 6),
    ("Noah", 23, "B", 3),
])
db_connection.commit()

print(f"Database and tables created successfully at: {DB_PATH}")
db_connection.close()