#!/usr/bin/python3
""" Defines a User class """
import sqlalchemy
from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5

class User(BaseModel):
    """ A class that represents a user and inherits from BaseModel """
"""    if models.storage == 'db':
        __tablename__ == 'users'
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        address = Column(String(128), nullable=False)
    else:
        first_name = ""
        last_name = ""
        email = ""
        password = ""
        address = """


