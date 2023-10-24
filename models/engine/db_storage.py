#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from os import getenv
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review


"""This module defines a class called DBStorage that represents the base
model to handle storage file"""


class DBStorage():
    """A class that handles the file storage of objects"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiation of DBStorage class"""

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(getenv('HBNB_MYSQL_USER'),
                                              getenv('HBNB_MYSQL_PWD'),
                                              getenv('HBNB_MYSQL_HOST'),
                                              getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns the dictionary __objects"""

        session = self.__session
        if cls is None:
            objs = session.query(State).all()
            objs.extend(session.query(City).all())
            objs.extend(session.query(User).all())
            objs.extend(session.query(Place).all())
            objs.extend(session.query(Amenity).all())
            objs.extend(session.query(Review).all())
        else:
            objs = session.query(cls).all()
        return {"{}.{}".format(type(obj).__name__, obj.id): obj for obj in objs}

    def new(self, obj):
        """Add the object to the current database session """

        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""

        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""

        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Method for deserializing the JSON file to objects"""

        self.__session.close()
