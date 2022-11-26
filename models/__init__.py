#!/usr/bin/python3
""" Instantiates FileStorage / DBStorage class """
import s
from models.engine.file_storage import FileStorage
from models.user import User
from models.review import Review
from models.meal_item import MealItem
from models.meal_category import MealCategory
from models.order import Order
from models.order_item import OrderItem

if os.getenv('MENJAR_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
