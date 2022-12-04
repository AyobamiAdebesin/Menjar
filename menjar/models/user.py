#!/usr/bin/python3
""" Defines a User class """
from models.base_model import BaseModel


class User(BaseModel):
    """ A class that represents a user and inherits from BaseModel """
    first_name = ""
    last_name = ""
    email = ""
    password = ""
    address = ""
