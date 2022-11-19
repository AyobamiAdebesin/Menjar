#!/usr/bin/python3
""" Defines a Review Class """
from base_model import BaseModel


class Review(BaseModel):
    """ Represents a review and inherits from BaseModel """
    user_id = ""
    text = ""
