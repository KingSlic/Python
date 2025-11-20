from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, mapped_column, Mapped,sessionmaker

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

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password
        }