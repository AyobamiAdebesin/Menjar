#!/usr/bin/python3
""" Defines a DB Storage """


class DBStorage:
    """ A class that manages the database storage of Menjar """
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a new model"""
        import os
        from sqlalchemy import create_engine
        from models.base_model import Base, BaseModel
        from models.user import User
        from models.review import Review
        from models.meal_item import MealItem
        from models.meal_category import MealCategory
        from models.order import Order
        from models.order_item import OrderItem

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            os.getenv('MENJAR_MYSQL_USER'), os.getenv('MENJAR_MYSQLPWD'),
            os.getenv('MENJAR_MYSQL_HOST'), os.getenv('MENJAR_MYSQL_DB')),
            pool_pre_ping=True)

        if os.getenv('MENJAR_ENV') == 'test':
            Base.metadata.dfrop_all(self.__engine)

    def all(self, cls=None):
        """ Returns a dictionary of models currently in storage """
        from models.user import User
        from models.review import Review
        from models.meal_item import MealItem
        from models.meal_category import MealCategory
        from models.order import Order
        from models.order_item import OrderItem
        new_dict = {}
        if cls is None:
            for item in self.__sesssion.query(User).all():
                key = item.__class__.__name__ + '.' + item.id
                new_dict[key] = item
            for item in self.__sesssion.query(Review).all():
                key = item.__class__.__name__ + '.' + item.id
                new_dict[key] = item
            for item in self.__sesssion.query(MealItem).all():
                key = item.__class__.__name__ + '.' + item.id
                new_dict[key] = item
            for item in self.__sesssion.query(MealCategory).all():
                key = item.__class__.__name__ + '.' + item.id
                new_dict[key] = item
            for item in self.__sesssion.query(Order).all():
                key = item.__class__.__name__ + '.' + item.id
                new_dict[key] = item
            for item in self.__sesssion.query(OrderItem).all():
                key = item.__class__.__name__ + '.' + item.id
                new_dict[key] = item

            else:
                for item in self.__session.query(cls).all():
                    key = "{}.{}".format(item.__class__.__name__, item.id)
                    new_dict[key] = item
            self.__session.close()
            return new_dict

    def new(self, obj):
        """ Adds a new object to storage """
        from sqlalchemy.orm import sessionmaker
        from models.user import User
        from models.review import Review
        from models.meal_item import MealItem
        from models.meal_category import MealCategory
        from models.order import Order
        from models.order_item import OrderItem
        self.__session.add(obj)

    def save(self):
        """ Commit all changes made to the database """
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        Create all tables in the database anytime the class
        is instantiated
        """
        from sqlalchemy.orm import scoped_session
        from sqlalchemy.orm import sessionmaker
        from models.base_model import Base, BaseModel
        from models.user import User
        from models.review import Review
        from models.meal_item import MealItem
        from models.meal_category import MealCategory
        from models.order import Order
        from models.order_item import OrderItem

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ Closes a session """
        self.__session.close_all()
