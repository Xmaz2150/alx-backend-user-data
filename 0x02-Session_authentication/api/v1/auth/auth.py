#!/usr/bin/env python3
"""
Authentication mdule
"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """
    Authentication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if path is not in excluded paths
        """
        if path and excluded_paths:
            if path[-1] != '/':
                path += '/'

            if path not in excluded_paths:
                return True
            else:
                return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """
        Checks authorization hearder in request
        """
        if request is None or 'Authorization' not in request.headers:
            return None

        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        My basic Basic Authentication (updated by next child)
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns sessions cookie value
        """

        if request:
            cookie_key = os.getenv('SESSION_NAME', None)

            return request.cookies.get(cookie_key)
        return None
