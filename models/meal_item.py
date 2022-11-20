#!/usr/bin/python3
""" Defines a Meal Item class """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey
from models.meal_category import MealCategory


class MealItem(BaseModel, Base):
    """ A class that represents a MealItem """
    __tablename__ = "meal_items"
    if os.getenv("MENJAR_STORAGE_TYPE") == "db":
        meal_name = Column(String(128), nullable=False)
        meal_categry_id = Column(
                String(60), ForeignKey('meal_category.id'),
                nullable=False)
        meal_price = Column(Integer(), nullable=False)
        isAvailable = True
    else:
        meal_name = ""
        meal_category_id = ""
        meal_price = 0
        isAvailable = True
