import sqlite3 

db_connection = sqlite3.connect("library.db")
db_connection.row_factory = sqlite3.Row

db_connection.execute("DROP TABLE IF EXISTS books")
db_connection.execute("DROP TABLE IF EXISTS authors")

authorsTable = """
    CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )    
"""

db_connection.execute(authorsTable)
db_connection.commit()

authors_query = "INSERT INTO authors (name) VALUES (?)"
db_connection.executemany(authors_query, [("Roald Dahl",), ("Brian Jacques",)])
db_connection.commit()



booksTable = """
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        year INTEGER,
        author_id INTEGER,
        FOREIGN KEY (author_id) REFERENCES authors(id)
    )

"""

db_connection.execute(booksTable)
db_connection.commit()

books_query = """
    INSERT INTO books (title, year, author_id) VALUES (?, ?, ?)
"""

db_connection.executemany(books_query, [
    ("BFG", 1982, 1),
    ("Taggerung", 2001, 2),
    ("James and the Giant Peach", 1961,  1),
    ("Salamandastron", 1992, 2)
])

db_connection.commit()

print("Database & tables created successfully")