#!/usr/bin/python3
""" Defines an order item """
from models.base_model import BaseModel


class OrderItem(BaseModel):
    """ Represents an Meal Item placed as an order """
    item_name = ""
    quantity = 0
    price = 0
