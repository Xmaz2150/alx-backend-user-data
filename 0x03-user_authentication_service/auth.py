#!/usr/bin/env python3
"""
Auhentication module
"""
import bcrypt
from db import DB
from user import User
from typing import TypeVar
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Encrypts password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """
        Registers user to DataBase
        """
        DB = self._db
        DB.add_user(email, _hash_password(password))
