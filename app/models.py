from sqlalchemy import Column, Integer, String
from flask_login import UserMixin
from app import lm, Base
from create_db import engine
from sqlalchemy.orm import sessionmaker


DBSession = sessionmaker(bind=engine)
session = DBSession()


class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False)
    email = Column(String(64), nullable=True)
    password = Column(String(150), nullable=True)


@lm.user_loader
def load_user(id):
    return session.query(User).get(int(id))
