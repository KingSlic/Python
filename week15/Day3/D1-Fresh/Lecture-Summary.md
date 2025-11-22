# Week 15, Day 3: Password Hashing and JWT Authentication

## Summary of Topics Covered

### 1. **Password Security & Hashing**

#### Why We Hash Passwords
- **The Problem**: Storing passwords as plain text is insecure. If your database gets hacked, all user passwords are exposed.
- **The Solution**: Hash passwords before storing them in the database.

#### Understanding Hashing vs Encryption
- **Hashing**: One-way transformation - you cannot reverse a hash back to the original password
- **Encryption**: Two-way transformation - you can decrypt to get the original value
- **Key Point**: Passwords should be hashed, NOT encrypted

#### How Password Hashing Works
1. User enters password (e.g., "mypassword123")
2. System hashes it → creates a long string (e.g., "$2b$12$abc123xyz...")
3. This hash is stored in the database
4. When user logs in again:
   - They enter their password
   - System hashes what they entered
   - Compares the two hashes
   - If they match → correct password

#### Salt: Extra Security Layer
- **What is Salt?**: A random string added to each password before hashing
- **Why Use Salt?**: Prevents rainbow table attacks (pre-computed hash databases)
- **Important**: Each user gets a unique salt, which is automatically included in the bcrypt hash

### 2. **Implementing Password Hashing with bcrypt**

#### Installation
```bash
pip install bcrypt
```

#### Hashing a Password (User Creation)
```python
import bcrypt

# Hash the password
hashed_password = bcrypt.hashpw(
    data['password'].encode('utf-8'),  # Convert to bytes
    bcrypt.gensalt()  # Generate salt
).decode('utf-8')  # Convert back to string for database storage

# Store hashed_password in database
user.password = hashed_password
```

#### Verifying a Password (Login)
```python
# Check if entered password matches stored hash
if bcrypt.checkpw(
    password.encode('utf-8'),  # User's entered password
    user.password.encode('utf-8')  # Hash from database
):
    # Password is correct
    return {"message": "Successful login"}
else:
    # Password is incorrect
    return {"error": "Invalid credentials"}
```

### 3. **HTTP Statelessness**

- **The Problem**: HTTP is stateless - the server doesn't remember previous requests
- Each request is independent; the server has no memory of who you are
- **The Solution**: Use tokens to identify users across requests

### 4. **JWT (JSON Web Tokens)**

#### What is JWT?
- A secure way to create tokens that contain user information
- The token is **signed** to prevent tampering
- The token can be **decoded** to read the information inside

#### JWT Structure
A JWT token contains three parts:
1. **Header**: Algorithm used
2. **Payload**: Data (claims) like user ID, expiration date
3. **Signature**: Ensures the token hasn't been altered

#### Installing JWT Library
```bash
pip install python-jose
```

### 5. **Implementing JWT Authentication**

#### Step 1: Generate Secret Key
```python
# At the top of your file
SECRET_KEY = "your-secret-key-here"  # Use a long, random string in production
```

#### Step 2: Create Token (During Login)
```python
from jose import jwt
from datetime import datetime, timedelta, timezone

# Prepare the payload
payload = {
    'exp': datetime.now(timezone.utc) + timedelta(minutes=30),  # Expiration
    'iat': datetime.now(timezone.utc),  # Issued at
    'sub': str(user.id),  # User ID (must be string!)
    'instructor': 'Ahmed'  # Any additional data
}

# Generate token
token = jwt.encode(
    payload,
    SECRET_KEY,
    algorithm='HS256'
)

# Return token to user
return {
    "message": "Successful login",
    "token": token,
    "type": "bearer"
}
```

#### Step 3: Verify Token (Protected Routes)
```python
# Read token from request header
auth_header = request.headers.get('Authorization')

if not auth_header or not auth_header.startswith('bearer'):
    return {"error": "Please provide the JWT token"}

# Extract token (remove "bearer " prefix)
token_without_bearer = auth_header.split(' ')[1]

# Decode and verify token
try:
    decoded_token = jwt.decode(
        token_without_bearer,
        SECRET_KEY,
        algorithms=['HS256']
    )
    # Token is valid - proceed with request
    # You can access user ID with: decoded_token['sub']
except:
    return {"error": "Failed to decode the token, please log in first"}
```

#### Step 4: Sending Token in Requests (Postman/Client)
In the **Headers** section:
- Key: `Authorization`
- Value: `bearer YOUR_TOKEN_HERE`

### 6. **Important Security Practices**

1. **Never store passwords as plain text**
2. **Always hash passwords before storing**
3. **Use standard libraries** (bcrypt, JWT) - don't create your own security
4. **Keep your SECRET_KEY private** - never share or commit it to version control
5. **Use strong secret keys** (32+ characters, random)
6. **Set appropriate token expiration times** (e.g., 30 minutes)
7. **Return generic error messages** ("Invalid credentials" instead of "User not found" or "Wrong password")

### 7. **Common Gotchas**

1. **Encoding/Decoding**: bcrypt requires bytes, so use `.encode('utf-8')` and `.decode('utf-8')`
2. **JWT Payload**: Values in the payload (especially `sub`) must be strings, not integers
3. **Bearer Token**: Include "bearer" before the token in the Authorization header
4. **Algorithm Parameter**: When decoding, pass `algorithms=['HS256']` as a list
5. **Token Expiration**: Tokens expire after the time you set - users need to login again

## Assignment

1. **Complete previous assignments** (Flask, ORM)
2. **Add authentication to your product/category app**:
   - Create a User model
   - Implement user creation (with password hashing)
   - Implement login (returns JWT token)
   - Protect at least one route (require JWT token)

## Key Takeaways

- **Security is critical** - never store plain passwords
- **Use established libraries** - bcrypt for hashing, JWT for tokens
- **Understand the concepts** - you should know what's happening, even if you reference code
- **Tokens enable stateless authentication** - users prove their identity with each request
- **Keep it simple** - use provided code as reference, understand what each part does

---

**Remember**: You don't need to memorize every line of code, but you should understand:
- Why we hash passwords
- How JWT tokens work
- When to use each piece (hashing during signup, checking during login, verifying tokens on protected routes)