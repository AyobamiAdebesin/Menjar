#!/usr/bin/python3
""" Defines a Meal Category """
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy import relationship


class MealCategory(BaseModel, Base):
    """ Represents a Meal Category Object """
    __tablename__ = "meal_categories"
    if os.get.env('MENJAR_TYPE_STORAGE') == "db":
        category_name = Column(String(128), nullable=False)
        meal_items = relationship(
                "MealItem", cascade="all, delete, delete-orphan",
                backref="meal_categories")
    else:
        category_name = ""

    def __init__(self, *args, **kwargs):
        """ Instantiates the MealItem class """
        from models.meal_item import MealItem
        super().__init__(*args, **kwargs)

    if os.getenv("MENJAR_TYPE_STORAGE") != "db":
        @property
        def meal_items(self):
            """ Get the meal items for a Meal Category from FileStorage """
            from models.meal_item import MealItem
            from models import storage
            meal_dict = storage.all(MealItem)
            meal_list = []
            for meal in meal_dict.values():
                if meal.meal_category_id == self.id:
                    meal_list.append(meal)
            return meal_list
