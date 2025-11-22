from sqlalchemy import create_engine, ForeignKey, Float
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, sessionmaker, relationship

engine = create_engine("sqlite:///store.db", echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)

class Category(Base):
    __tablename__ = 'categories'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    
    category: Mapped["Category"] = relationship("Category", back_populates="products")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category_id": self.category_id
        }
        
    
        
