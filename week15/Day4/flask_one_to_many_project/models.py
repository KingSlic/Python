from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker, relationship
import bcrypt


engine = create_engine("sqlite:///notes.db", echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    notes: Mapped[list["Note"]] = relationship("Note", back_populates="user")


    def set_password(self, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.password = hashed_password

    def check_password(self, password):
        raw_pw_bytes = password.encode('utf-8')
        stored_hash_bytes = self.password.encode('utf-8')
        return bcrypt.checkpw(raw_pw_bytes, stored_hash_bytes)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }
    

class Note(Base):
    __tablename__ = "notes"

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
            "user_id": self.user_id
        }
