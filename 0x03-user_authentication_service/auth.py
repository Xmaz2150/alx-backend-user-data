#!/usr/bin/env python3
"""
Auhentication module
"""
from sqlalchemy.orm.exc import NoResultFound

import bcrypt
import uuid
from typing import TypeVar
from db import DB


def _hash_password(password: str) -> bytes:
    """
    Encrypts password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Generates uuid 4
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """
        Registers user if they exist
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates user's password
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Creates session for existing user
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user_id = user.id

            self._db.update_user(user_id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
