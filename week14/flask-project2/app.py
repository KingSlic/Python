from flask import Flask
import sqlite3

app = Flask(__name__)

def get_db():
    db_conn = sqlite3.connect("my_database.db")
    db_conn.row_factory = sqlite3.Row
    return db_conn


@app.route("/")
def hello_world():
    return "<h1>Hello, World!</h1>"


@app.route("/authors")
def authors():
    db = get_db()
    cur = db.execute("SELECT * FROM authors")
    rows = cur.fetchall()
    db.close()

    return [dict(author) for author in rows]

    # authors_list = []
    # for author in rows:
    #     authors_list.append(dict(author))

    # return authors_list


@app.route("/authors")
def get_books_func():
    # get database connection object
    db = get_db()

    # query books table to fetch all books
    rows = db.execute("SELECT * FROM books").fetchall()

    # create an empty list to store the modified books dictionaries
    books_list = []
    for book in rows:
        book_dict = dict(book)

        # Query authors table to get book author of the current iteration
        author = db.execute(f"SELECT * FROM authors WHERE id={book_dict["author_id"]}").fetchone()
        
        # Convert the author row to a dictionary
        author_dict = dict(author)

        # Add author name to the book dictionary
        book_dict["authorName"] = author_dict["name"]

        # Add the modified book dictionary to the books list
        books_list.append(book_dict)

    # Close the database connection 
    db.close()

    # Return the list of books ( list of dicts )
    return books_list