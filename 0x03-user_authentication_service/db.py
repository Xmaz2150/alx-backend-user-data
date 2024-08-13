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
        cols = [str(c) for c in User.__table__.columns]

        for k in search.keys():
            if 'users.{}'.format(k) not in cols:
                raise InvalidRequestError

        user = self._session.query(User).filter_by(**search).first()
        if not user:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **search) -> None:
        """
        Updates user
        """

        try:
            user = self.find_user_by(id=user_id)

            for k, v in search.items():
                if hasattr(user, k):
                    setattr(user, k, v)
                else:
                    raise ValueError
            self._session.commit()
        except NoResultFound:
            pass
        return None
