#!/usr/bin/python3
""" Defines a Meal Item class """
from base_model import BaseModel


class MealItem(BaseModel):
    """ A class that represents a MealItem """
    meal_name = ""
    meal_category = ""
    meal_price = 0
    isAvailable = True
