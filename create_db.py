#!/usr/bin/python
from app import app
from sqlalchemy import create_engine
from app.models import Base

engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])

Base.metadata.create_all(engine)
