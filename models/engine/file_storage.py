#!/usr/bin/python3
""" Defines a File Storage Class """
import json

__session = None

class FileStorage:
    """ Represents a FileStorage System """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ Returns the dict __objects"""
        return (FileStorage.__objects)

    def new(self, obj):
        """ Adds a new element obj to the FileStorage.__objects dict """
        if obj:
            obj_id = obj.__class__.__name__ + "." + obj.id
            FileStorage.__objects[obj_id] = obj

    def save(self):
        """
        Serializes all objects in __objects to the JSON  file; __file_path
        """
        json_object = {}
        for key, obj in FileStorage.__objects.items():
            json_object[key] = obj.to_dict()

        with open(FileStorage.__file_path, 'w', encoding='utf-8') as f:
            json.dump(json_object, f)

    def reload(self):
        """ Deserializes the JSON file to objects """
        from models.base_model import BaseModel
        from models.user import User
        from models.meal_item import MealItem
        from models.meal_category import MealCategory
        from models.review import Review
        from models.order import Order
        from models.order_item import OrderItem

        class_dict = {
                "BaseModel": BaseModel, "User": User, "MealItem": MealItem,
                "MealCategory": MealCategory, "Review": Review,
                "Order": Order, "OrderItem": OrderItem
                }
        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                json_object = json.load(f)
            for key, value, in json_object.items():
                class_name = value['__class__']
                if class_name in class_dict:
                    model_name = class_dict.get(class_name)
                    self.new(model_name(**value))
        except FileNotFoundError:
            pass
    def close(self):
        self.__session.close_all()
