#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        create a user instance
        """
        session = self._session
        user = User(email=email, hashed_password=hashed_password)
        try:
            session.add(user)
            session.commit()
            return user
        except Exception:
            session.rollback()
            user = None
            return user

    def find_user_by(self, **kwargs) -> User:
        """
        find user
        """

        session = self._session
        if not kwargs:
            raise InvalidRequestError

        for key in kwargs.keys():
            if not hasattr(User, key):
                raise InvalidRequestError

        user = session.query(User).filter_by(**kwargs).first()
        if user:
            return user
        else:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        update user
        """

        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError
            setattr(user, key, value)

        self._session.commit()
