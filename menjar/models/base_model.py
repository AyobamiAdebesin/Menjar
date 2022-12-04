#!/usr/bin/python3
""" A script that contains the Base Model class
for all objects in this program
"""
import uuid
import os
import sys

from datetime import timezone
from datetime import datetime
#from models import storage
from sqlalchemy import Column, DateTime, String
from sqlalchemy import Text,Table
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base


my_metadata = MetaData()
Base = declarative_base(metadata=my_metadata)


class BaseModel:
    """ Base Model for all classes """
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(
            DateTime(timezone=False),
            nullable=False, default=datetime.now())
    updated_at = Column(
            DateTime(timezone=False),
            nullable=False, default=datetime.now())

    def __init__(self, *args, **kwargs):
        """ Initializes attributes from *args and **kwargs """
        if kwargs == {} and len(kwargs) == 0:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        elif '__class__' in kwargs.keys():
            kwargs['updated_at'] = datetime.fromisoformat(
                    kwargs['updated_at'])
            kwargs['created_at'] = datetime.fromisoformat(
                    kwargs['created_at'])
            del kwargs['__class__']
            self.__dict__update(kwargs)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            self.__dict__.update(kwargs)

        """
        if kwargs:
            for k, v in kwargs.items():
                if k == "__class__":
                    pass
                elif k == "created_at":
                    self.created_at = datetime.fromisoformat(v)
                elif k == "updated_at":
                    self.updated_at = datetime.fromisoformat(v)
                else:
                    setattr(self, k, v)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)
        """

    def __str__(self):
        """ String representation of the BaseModel """
        dictionary = {}
        dictionary.update(self.__dict__)
        if '_sa_instance_state' in dictionary.keys():
            del dicctionary['_sa_instance_state']
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, dictionary)

        """
        return "[{}] ({}) {}".format(
                self.__class__.__name__,
                self.id, self.__dict__)
        """

    def save(self):
        """ Updates the public instance attribute updated_at
        with the current datetime """
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """
        Returns a dictionary containing all key/value of
        the __dict__ attribute of the instance"""
        new_dict = self.__dict__.copy()
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = new_dict['created_at'].isoformat()
        new_dict['updated_at'] = new_dict['updated_at'].isoformat()
        return (new_dict)

    def delete(self):
        """ Delete an instance """
        from models import storage
        storage.delete(self)
