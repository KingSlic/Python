CREATE TABLE authors (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    created_at TEXT DEFAULT
    (datetime('now'))
)

INSERT INTO authors (name, email) VALUES("Roald Dahl", "rdahl@gmail.com")
INSERT INTO authors (name, email) VALUES("Stephen King", "horrormaster@gmail.com")

