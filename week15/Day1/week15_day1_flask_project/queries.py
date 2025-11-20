import sqlite3
from sqlalchemy import create_engine, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column, relationship


engine = create_engine("sqlite:///school_db.db", echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Teacher(Base):
    __tablename__ = "teachers"
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False)
    
    students: Mapped[list["Student"]] = relationship("Student", back_populates="teacher")
    
    