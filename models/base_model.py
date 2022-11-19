#!/usr/bin/python3
""" A script that contains the Base Model class
for all objects in this program
"""
import uuid
import datetime
import os
import sys
import sqlaclchemy
from sqlalchemy.ext import declarative_base


class BaseModel:
    """ Base Model for all classes """
    def __init__(self, *args, **kwargs):
        """ Initializes attributes from *args and **kwargs """
        if kwargs:
            for k, v in kwargs.items():
                if k == "__class__":
                    pass
                elif k == "created_at":
                    self.created_at = datetiime.fromisoformat(value)
                elif k == "updated_at":
                    self.updated_at = datetime.fromisoformat(value)
                else:
                    setattr(self, k, v)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """ String representation of the BaseModel """
        return "[{}] ({}) {}".format(
                self.__class__.__name__,
                self.id, self.__dict__)

    def save(self):
        """ Updated the public instance attribute updated_at
        with the current datetime """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """
        Returns a dictionary containing all key/value of
        the __dict__ attribute of the instance"""
        new_dict = self.__dict__.copy()
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = new_dict['created_at'].isoformat()
        new_dict['updated_at'] = new_dict['updated_at'].isformat()
