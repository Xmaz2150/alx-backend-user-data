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

        Session = self._session
        Session.add(user)
        Session.commit()
        return user

    def find_user_by(self, **search) -> TypeVar('User'):
        """
        Queries user
        """
        cols = [str(c) for c in User.__table__.columns]

        if 'users.{}'.format(*search) not in cols:
            raise InvalidRequestError

        Session = self._session
        user = Session.query(User).filter_by(**search).one()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **search) -> None:
        """
        Updates user
        """

        cols = [str(c) for c in User.__table__.columns]
        for k in search.keys():
            if 'users.{}'.format(k) not in cols:
                raise ValueError

        Session = self._session
        Session.query(User).filter_by(id=user_id).update(search)
        Session.commit()
