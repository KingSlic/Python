from sqlalchemy import create_engine, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, mapped_column, Mapped,sessionmaker, relationship
from datetime import datetime

# Think of it as the database connection
engine = create_engine("sqlite:///database.db", echo=True)
# Declarative base is the base class of all of our models
Base = declarative_base()
# Session maker is the tool that will allow us to interact with the database
Session = sessionmaker(bind=engine)

class User(Base):
    # Table name in database
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    # Define the relationship between user and posts
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="creator")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }
    

class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Define the relationship between the Post and the User classes
    creator: Mapped["User"] = relationship("User", back_populates="posts")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }