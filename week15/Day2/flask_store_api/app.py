from flask import Flask, request, jsonify
from models import Session, Category, Product

app = Flask(__name__)

#Step 1: Create a session
#Step 2: Query/modify DB using SQLAlchemy
#Step 3: Commit if needed
#Step 4: Close the session



@app.route("/categories", methods=["GET"])
def get_categories():
    
    session = Session()
    items = session.query(Category).all()
    session.close()
    return jsonify([item.to_dict() for item in items])


@app.route("/products", methods=["GET"])
def get_products():
    
    session = Session()
    products = session.query(Product).all()
    session.close()
    return jsonify([product.to_dict() for product in products])


@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    
    session = Session()
    product = session.query(Product).filter_by(id=id).first()
    if product is None:
        session.close()
        return jsonify({"error": "product not found"}), 404
    
    result = product.to_dict()
    session.close()
    return jsonify(product.to_dict()), 200


@app.route("/categories", methods=["POST"])
def create_category():
    data = request.get_json()
    name = data.get("name")
    
    if not name:
        return {"error": "name is required"}, 400
    
    session = Session()
    category = Category(name=name)
    session.add(category)
    session.commit()
    session.close()
    
    return category.to_dict(), 201


@app.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    name = data.get("name")
    price = data.get("price")
    category_id = data.get("category_id")
    
    if not name:
        return {"error": "name is required"}, 400
    if price is None:
        return {"error": "price is required"}, 400
    if not category_id:
        return {"error": "category_id is required"}, 400
    
    session = Session()
    
    category = session.query(Category).filter_by(id=category_id).first()
    if not category:
        session.close()
        return {"error": "Category not found"}, 404
    
    product = Product(name=name, price=price, category_id=category_id)
    session.add(product)
    session.commit()
    session.close()
    
    return product.to_dict(), 201


@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    data = request.get_json()

    session = Session()
    product = session.query(Product).filter_by(id=id).first()
    if not product:
        session.close()
        return {"error": "product not found"}, 404

    product.name = data.get("name", product.name)
    product.price = data.get("price", product.price)
    product.category_id = data.get("category_id", product.category_id)

    session.commit()
    session.close()

    return product.to_dict(), 200


@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    session = Session()
    product = session.query(Product).filter_by(id=id).first()

    if not product:
        session.close()
        return {"error": "product not found"}, 404

    session.delete(product)
    session.commit()
    session.close()

    return product.to_dict(), 200