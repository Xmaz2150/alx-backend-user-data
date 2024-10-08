#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User
from typing import TypeVar


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
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

    def add_user(self, email: str, hashed_password: str) -> TypeVar('User'):
        """
        Adds user to session
        """
        user = User(email=email, hashed_password=hashed_password)

        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **search) -> TypeVar('User'):
        """
        Queries user
        """
        cols = User.__table__.columns.keys()

        for k in search.keys():
            if k not in cols:
                raise InvalidRequestError

        try:
            return self._session.query(User).filter_by(**search).one()
        except NoResultFound:
            raise NoResultFound

    def update_user(self, user_id: int, **search) -> None:
        """
        Updates user
        """

        cols = User.__table__.columns.keys()

        for k in search.keys():
            if k not in cols:
                raise ValueError

        user = self.find_user_by(id=user_id)
        for k, v in search.items():
            setattr(user, k, v)
        self._session.commit()
