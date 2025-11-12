# from flask import Flask, jsonify
# import sqlite3

# app = Flask(__name__)
    

# def get_db():
#     db_conn = sqlite3.connect("my_database.db")
#     db_conn.row_factory = sqlite3.Row
#     return db_conn


# @app.route("/")
# def hello_world():
#     return "<p>Hello World</p>"


# @app.route("/authors")
# def authors():
#     db = get_db()
#     cur = db.execute("SELECT * FROM authors")
#     rows = cur.fetchall()
#     db.close()
    
#     return [dict(author) for author in rows]


# @app.route("/books")
# def get_books_func():
#     # get database connection object
#     db = get_db()
    
#     # query books table to fetch all books
#     rows = db.execute("SELECT * FROM books").fetchall()
#     # db.close()
    
#     # return [dict(book) for book in rows]
    
#     # create an empty list to store the modified books dictionaries
#     books_list = []
#     for book in rows:
#         book_dict = dict(book)
    
        
#         # Query author's table to get author with id=author_id
#         # SELECT * FROM authors WHERE id=1
#         author = db.execute(f"SELECT * FROM authors WHERE id={book_dict["author_id"]}").fetchone() #Gives us a single row
#         author_dict = dict(author)
#         book_dict["authorName"] = author_dict["name"]
        
#         books_list.append(book_dict)
        
#     db.close()
    
#     return jsonify(books_list)


# class Row:
#     pass

# dict(Row())

# rows = []
# rows.append(Row())
# rows.append(Row())
# rows.append(Row())

from flask import Flask
import sqlite3

app = Flask(__name__)


# Step 1: connect the database
def get_db():
    db_conn = sqlite3.connect("library_database.db")
    
    #Returns each row as an object that's both tuple & dictionary
    db_conn.row_factory = sqlite3.Row
    return db_conn

#Step 2: Create your routes

@app.route("/")
def welcome():
    return "<h1>Welcome to my first Flask page!"

@app.route("/authors")
def authors():
    #Call the database
    db = get_db()
    #Execute a query 
    cur = db.execute("SELECT * FROM authors")
    rows = cur.fetchall()
    db.close()
    
    authors_list = []
    for author in rows:
        authors_list.append(dict(author))
        
    return authors_list


@app.route("/authors")
def get_books():
    db = get_db()
    
    rows = db.execute("SELECT * FROM books").fetchall()
    
    #create empty list to store books dictionaries
    books_list = []
    for book in rows:
        book_dict = dict(book)
        
        #Query the author's table to get the current book's author
        author = db.execute(f"SELECT * FROM authors WHERE id={book_dict["author_id"]}").fetchone()
        
        #Turn author row into a dictionary
        author_dict = dict(author)
        
        #Add author name to books dictionary (authorName column)
        book_dict["authorName"] = author_dict["name"]
        
        