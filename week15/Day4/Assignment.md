# **Assignment: Flask API with Authentication + One-to-Many**

## 🎯 **Goal**

Build a small Flask API with:

* **User authentication** using JWT
* A one-to-many relationship (**User → Notes**)
* CRUD for notes **restricted to the logged-in user**
* No many-to-many, no tags, no advanced features — just clean, practical ORM + auth.

---

# 📁 **Models Required (`models.py`)**

Create **two models**:

### ### **1. User**

| Field    | Type         | Notes             |
| -------- | ------------ | ----------------- |
| id       | int          | PK                |
| name     | str          | required          |
| email    | str          | required + unique |
| password | str          | hashed password   |
| notes    | relationship | One-to-many       |

Methods:

* `set_password()`
* `check_password()`
* `to_dict()` (NO PASSWORD)

---

### ### **2. Note**

| Field   | Type | Notes           |
| ------- | ---- | --------------- |
| id      | int  | PK              |
| title   | str  | required        |
| content | str  | required        |
| user_id | FK   | belongs to User |

Methods:

* `to_dict()`

---

# 🔑 **Authentication Requirements**

Implement:

### **POST `/register`**

Create a new user.

### **POST `/login`**

Verify password → return JWT token.

### `get_logged_in_user_id()`

Copy from your example to decode token and return the user ID.

---

# 📝 **Assignments Tasks (Short but Valuable)**

## ### **1. GET `/me`**

Return the currently logged-in user.

**Only accessible with a valid token.**

Response:

```json
{
  "id": 1,
  "name": "Ahmed",
  "email": "ahmed@example.com"
}
```

---

## ### **2. POST `/notes`** (AUTH REQUIRED)

Create a new note **for the logged-in user only**.

Request:

```json
{
  "title": "Shopping list",
  "content": "Milk, pizza, chocolate"
}
```

Validations:

* title required
* content required

Response:

```json
{
  "id": 1,
  "title": "Shopping list",
  "content": "Milk, pizza, chocolate",
  "user_id": 2
}
```

---

## ### **3. GET `/notes`** (AUTH REQUIRED)

Return **all notes belonging to the logged-in user**.

---

## ### **4. GET `/notes/<id>`** (AUTH REQUIRED)

Return a single note **only if it belongs to the logged-in user**.

If the note belongs to a different user → return:

```json
{"error": "not allowed"}
```

---

## ### **5. PUT `/notes/<id>`** (AUTH REQUIRED)

User can update **their own notes only**.

Validations:

* title required
* content required

---

## ### **6. DELETE `/notes/<id>`** (AUTH REQUIRED)

Delete a note, but only if it belongs to the user.

---

# 🎯 **What Students Must Practice**

✔ Using JWT tokens
✔ Creating protected routes
✔ Restricting access by user ownership
✔ SQLAlchemy one-to-many relationships
✔ Validation & error handling
✔ Clean JSON responses
✔ Reusing logic from the last lecture

---

# 🧪 **Example Workflow for Students to Test**

1. Register → `/register`
2. Login → receive JWT token
3. Add token to `Authorization: Bearer <token>`
4. Create notes
5. Fetch notes
6. Try accessing notes from other users → should be forbidden

---

# 🏁 **Deliverables**

Students must submit:

* `models.py`
* `app.py`
* `notes.db`