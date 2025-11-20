import sqlite3

db_connection = sqlite3.connect("school_db.db")

db_connection.execute("DROP TABLE IF EXISTS books")
db_connection.execute("DROP TABLE IF EXISTS authors")
db_connection.commit()

teachersTable = """
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
"""

db_connection.execute(teachersTable)
db_connection.commit()


db_connection.executemany(
    "INSERT INTO teachers (name) VALUES (?)",
    [
        ("Zachary Taylor",),
        ("James Tyler",),
        ("Ulysses Grant",),
        ("William MckInley",),
    ]
)
db_connection.commit()


studentsTable = """
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade INTEGER NOT NULL,
        teacher_id INTEGER NOT NULL
        FOREIGN KEY (teacher_id) REFERENCES teachers(id)
    )
"""
db_connection.commit()

students_query = """
    INSERT INTO students (name, age, grade, teacher_id) VALUES (?, ?, ?, ?)
"""

db_connection.executemany(students_query, [
    ("Ada", 21, "A", 2),
    ("Bickford", 20, "B", 1),
    ("Cassandra", 22, "A", 3),
    ("Dominic", 19, "D", 4),
    ("Jack", 22, "A", 1),
    ("Kara", 21, "A", 2),
    ("Liam", 23, "B", 4),
])
db_connection.commit()

print(f"Database and tables created successfully")