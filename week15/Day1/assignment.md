# Python Flask Assignment 

## **Build a Flask + SQLite CRUD API With Validation and One-to-Many Relationships**

---

## 🎯 **Objective**

In this assignment, you will build a complete Flask API from scratch.
You will:

* Create a **SQLite database with two related tables**
* Implement **CRUD** operations (Create, Read, Update, Delete)
* Use a **1-to-many relationship** (authors → books)
* Add **basic validation** and return **structured JSON errors**
* Use Flask’s built-in development server
* Use SQL queries with the `sqlite3` module (no ORM)

No starter code is provided — you must create all files yourself.

---

# 🧩 Step 1 — Project Setup

### 1. Create a Project Folder

```bash
mkdir my_flask_project
cd my_flask_project
```

### 2. Create and Activate Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Flask

```bash
pip install flask
```

---

# 🗃️ Step 2 — Create the SQLite Database (`init_db.py`)

Create a file named **`init_db.py`**.
In this file:

## **A. Create a SQLite database**

Use Python's built-in `sqlite3` module to create **library.db**.

---

## **B. Create the following tables:**

### **1. authors table**

| column | type    | notes                      |
| ------ | ------- | -------------------------- |
| id     | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| name   | TEXT    | NOT NULL                   |

### **2. books table**

| column    | type    | notes                      |
| --------- | ------- | -------------------------- |
| id        | INTEGER | PRIMARY KEY, AUTOINCREMENT |
| title     | TEXT    | NOT NULL                   |
| year      | INTEGER | optional                   |
| author_id | INTEGER | FOREIGN KEY → authors.id   |

---

## **C. Insert sample data**

### Insert at least:

* **2 authors**
* **4 books**, each linked to an author through `author_id`

---

## **D. Run the script:**

```bash
python init_db.py
```

You should see a new file created:

```
library.db
```

---

# 🌐 Step 3 — Create the Flask App (`app.py`)

1. Create **app.py**
2. Import:

   * `Flask`
   * `request`
   * `jsonify`
   * `sqlite3`
3. Create a Flask app instance
4. Add a test route:

### Example:

```python
@app.route("/")
def home():
    return "Hello Flask!"
```

5. Run the server:

```bash
flask --app app run --reload
```

6. Visit:
   [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

# 🔍 Step 4 — API Requirements

Your API must include **all** the following routes.

---

# 📘 READ Routes (GET)

## 1. **GET `/authors`**

Returns all authors.

### Example success response:

```json
[
  {"id": 1, "name": "Author One"},
  {"id": 2, "name": "Author Two"}
]
```

---

## 2. **GET `/books`**

Returns all books.

### Example:

```json
[
  {"id": 1, "title": "Book A", "year": 2000, "author_id": 1},
  {"id": 2, "title": "Book B", "year": 2002, "author_id": 1}
]
```

---

## 3. **GET `/books/<id>`**

Return a single book by ID.

### If book exists:

```json
{"id": 1, "title": "Book A", "year": 2000, "author_id": 1}
```

### If book does NOT exist:

```json
{"error": "book not found"}
```

HTTP status: **404**

---

## 4. **GET `/authors/<author_id>/books`**

Return all books for a specific author.

### If author exists:

```json
[
  {"id": 3, "title": "Novel One", "year": 2019, "author_id": 2},
  {"id": 4, "title": "Novel Two", "year": 2020, "author_id": 2}
]
```

### If author does NOT exist:

```json
{"error": "author not found"}
```

Status: **404**

---

# ✍️ CREATE Route (POST)

## **POST `/books`**

Creates a new book.

### Expected JSON body:

```json
{
  "title": "New Book",
  "year": 2024,
  "author_id": 1
}
```

---

## **Validation Rules:**

| Field     | Required? | Validation                        |
| --------- | --------- | --------------------------------- |
| title     | YES       | Must be non-empty string          |
| year      | optional  | Must be an integer if provided    |
| author_id | YES       | Must reference an existing author |

---

## ✔️ Example success response:

```json
{
  "message": "book created",
  "book": {
    "id": 7,
    "title": "New Book",
    "year": 2024,
    "author_id": 1
  }
}
```

---

## ❌ Validation failure examples:

### Missing title:

```json
{"error": "title is required"}
```

### Invalid year:

```json
{"error": "year must be an integer"}
```

### Non-existent author:

```json
{"error": "author not found"}
```

Status code for all validation errors: **400**

---

# ✏️ UPDATE Route (PUT)

## **PUT `/books/<id>`**

Updates any of these fields:

* `title`
* `year`
* `author_id`

Uses the **same validation as POST**.

---

## ✔️ Example success response:

```json
{
  "message": "book updated",
  "book": {
    "id": 3,
    "title": "Updated Name",
    "year": 2021,
    "author_id": 2
  }
}
```

---

## ❌ If book doesn’t exist:

```json
{"error": "book not found"}
```

Status: **404**

---

## ❌ Validation errors (examples):

```json
{"error": "title cannot be empty"}
```

```json
{"error": "author not found"}
```

```json
{"error": "year must be an integer"}
```

Status: **400**

---

# ❌ DELETE Route

## **DELETE `/books/<id>`**

Deletes a book.

### ✔️ Success:

```json
{"message": "book deleted"}
```

### ❌ If book does not exist:

```json
{"error": "book not found"}
```

Status: **404**

---

# 🛡 Additional API Requirements

### All responses must be valid JSON.

Use:

```python
return jsonify(data), status_code
```

---

### Every database operation must:

* Open a connection inside the route
* Use parameterized queries (avoid SQL injection)
* Close the connection

---

### All error messages must follow this pattern:

```json
{"error": "description here"}
```

---

# 📄 Deliverables Checklist

You must submit:

### ✔️ `init_db.py`

* Creates tables
* Inserts sample data

### ✔️ `library.db`

* Generated database

### ✔️ `app.py`

Contains:

* All CRUD routes
* One-to-many route (`/authors/<id>/books`)
* Validation logic
* Error handling

### ✔️ Screenshots

1. Flask server running
2. Browser or Postman:

   * `/authors`
   * `/books`
   * `/books/<id>`
   * POST example
   * PUT example
   * DELETE example

---

# 🏁 Learning Outcomes

After completing this assignment, you will understand:

* Flask routing
* SQLite database creation
* SQL queries using Python
* CRUD operations
* JSON API design
* Data validation
* Relational data (1-to-many)
