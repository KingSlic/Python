from flask import Flask, request, jsonify
from models import Session, Category, Product

app = Flask(__name__)

#Step 1: Create a session
#Step 2: Query/modify DB using SQLAlchemy
#Step 3: Commit if needed
#Step 4: Close the session



@app.route("/categories")
def get_categories():
    
    session = Session()
    items = session.query(Category).all()
    session.close()
    return jsonify([item.to_dict() for item in items])


@app.route("/products")
def get_products():
    
    session = Session()
    products = session.query(Product).all()
    session.close()
    return jsonify([product.to_dict() for product in products])


@app.route("/products/<int:id>")
def get_product(id):
    
    session = Session()
    product = session.query(Product).filter_by(id=id).first()
    if product is None:
        session.close()
        return jsonify({"error": "product not found"}), 404
    
    result = product.to_dict()
    session.close()
    return jsonify([product.to_dict()]), 200


