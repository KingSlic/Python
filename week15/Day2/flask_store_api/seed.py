from models import Session, Base, engine, Category, Product

Base.metadata.create_all(engine)

session = Session()

electronics = Category(name="Electronics")
clothing = Category(name="Clothing")

session.add_all([electronics, clothing])
session.commit()

laptop = Product(name="Laptop", price=999.99, category_id=1)
mouse = Product(name="Mouse", price=25.50, category_id=1)
shirt = Product(name="T-shirt", price=19.99, category=clothing)
jeans = Product(name="Jeans", price=49.99, category=clothing)

session.add_all([laptop, mouse, shirt, jeans])
session.commit()

print("Database seeded!")
session.close()