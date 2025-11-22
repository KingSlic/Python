from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, sessionmaker, relationship

engine = create_engine("sqlite:///notes.db", echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    notes: Mapped[list["Note"]] = relationship(back_populates="user")
    
    
    def get_password():
        pass
    
    def set_password():
        pass
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
    
    
class Note(Base):
    __tablename__ = 'notes'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    user: Mapped["User"] = relationship("User", back_populates="notes")
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id,
        }
    
    