from flask import Flask, request, jsonify
import sqlite3
import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True


def get_db():
    db_conn = sqlite3.connect("library.db")
    db_conn.row_factory = sqlite3.Row
    return db_conn

# Step 2: Create your routes

@app.route("/")
def home():
    return "Welcome to my Flask!"


@app.route("/authors", methods=["GET"])
def get_authors():
    db = get_db()
    writers = db.execute("SELECT * FROM authors")
    rows = writers.fetchall()
    db.close()
    
    authors_list = [dict(author) for author in rows]
    return jsonify(authors_list), 200


@app.route("/books", methods=['GET'])
def get_books():
    
    db = get_db()
    books = db.execute("SELECT * FROM books").fetchall()
    db.close()
    
    books_list = [dict(row) for row in books]
    return jsonify(books_list), 200
    
    # data = request.get_json()
    
    # if "author_id" not in data:
    #     return jsonify({"error": "author not found"}), 400
    
    # if "title" not in data:
    #     return jsonify({"error": "title is required"}), 400
    
    # if "year" not in data:
    #     return jsonify({"error": "year must be an integer"}), 400
    
    # author_id = data["author_id"]
    # book_title = data["title"]
    # book_year = data["year"]
   
 
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book_id(book_id):
    db = get_db()
    book = db.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    db.close()
    
    if book is None:
        return jsonify({"error": "book not found"}), 404
    
    return jsonify(dict(book)), 200


#Returns all books for a specific author
@app.route("/authors/<int:author_id>", methods=["GET"])
def get_books_by_author(author_id):
    db = get_db()
    
    #Check whether author exists
    author = db.execute("SELECT * FROM authors WHERE id = ?", (author_id,)).fetchone()
    if author is None:
        db.close()
        return jsonify({"error": "author not found"}), 404
    
    books = db.execute("SELECT * FROM books WHERE author_id = ?", (author_id,)).fetchall()
    db.close()
    
    books_list = [dict(row) for row in books]
    return jsonify(books_list), 200


#Create the route with POST method
@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json() or {}
    
    title = data.get("title")
    year = data.get("year")
    author_id = data.get("author_id")
    
    if not title or not title.strip():
        return jsonify({"error": "title is required"}), 400

    if year is not None:
        try:
            year = int(year)
        except (TypeError, ValueError):
            return jsonify({"error": "year must be an integer"}), 400
    
    
    if author_id is None:
        return jsonify({"error": "author_id is required"}), 400
    
    try:
        author_id = int(author_id)
    except(TypeError, ValueError):
        return jsonify({"error": "author_id must be an integer"}), 400
    
    db = get_db()
    author = db.execute("SELECT * FROM authors WHERE id = ?", (author_id,)).fetchone()
    
    if author is None:
        db.close()
        return jsonify({"error": "author not found"}), 400
    
    
    insert_book = db.execute("INSERT INTO books (title, year, author_id) VALUES (?, ?, ?)", (title.strip(), year, author_id))
    db.commit()
    
    new_book_id = insert_book.lastrowid
    
    new_book = db.execute("SELECT * FROM books WHERE id = ?", (new_book_id,)).fetchone()
    
    db.close()
    
    
    return jsonify({
        "message": "book created",
        "book": dict(new_book)    
    }), 201


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book_id(book_id):
    
    data = request.get_json() or {}

    db = get_db()
    exists = db.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()

    if exists is None:
        db.close()
        return jsonify({"error": "book not found"}), 404

    current = dict(exists)

    title = data.get("title", current["title"])
    year = data.get("year", current["year"])
    author_id = data.get("author_id", current["author_id"])

    if "title" in data:
        if not title or not title.strip():
            db.close()
            return jsonify({"error": "title cannot be empty"}), 400

    if "year" in data:
        if year is not None:
            try:
                year = int(year)
            except (TypeError, ValueError):
                db.close()
                return jsonify({"error": "year must be an integer"}), 400

    if "author_id" in data:
        try:
            author_id = int(data["author_id"])
        except (TypeError, ValueError):
            db.close()
            return jsonify({"error": "author_id must be an integer"}), 400

        author = db.execute("SELECT * FROM authors WHERE id=?", (author_id,)).fetchone()

        if author is None:
            db.close()
            return jsonify({"error": "author not found"}), 400

    db.execute(
        """
        UPDATE books
        SET title = ?, year = ?, author_id = ?
        WHERE id = ?
        """,
        (title.strip(), year, author_id, book_id),
    )
    db.commit()

    updated_book = db.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    db.close()

    return jsonify({
        "message": "book updated",
        "book": dict(updated_book)
    }), 200




@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    db = get_db()
    book = db.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    
    if book is None:
        db.close()
        return jsonify({"error": "book not found"}), 404
    
    db.execute("DELETE FROM books WHERE id = ?", (book_id,))
    db.commit()
    db.close()
    
    return jsonify({"message": "book deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)