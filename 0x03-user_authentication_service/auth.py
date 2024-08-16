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

    def get_user_from_session_id(self, session_id: str) -> TypeVar('User'):
        """
        Gets user by session id
        """
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys user's session
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Creates password reset token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            user_id = user.id

            self._db.update_user(user_id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates user's password provide they reset token
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            new_hash = _hash_password(password)
            self._db.update_user(
                    user.id,
                    hashed_password=new_hash,
                    reset_token=None
                    )
        except NoResultFound:
            raise ValueError
