#!/usr/bin/env python3
"""
Basic Authentication mdule
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
from base64 import b64decode
import binascii


class BasicAuth(Auth):
    """
    Basic Authentication class
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Reurns encoded authorization header
        """
        if authorization_header is None or not isinstance(authorization_header, str) or authorization_header.split(' ')[0] != 'Basic':
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        returns base64 decoded  authorization header
        """
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        else:
            try:
                decodedb64 = b64decode(base64_authorization_header)

                return decodedb64.decode('utf-8')
            except binascii.Error:
                return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        extracts user credentials from base64 dedode string
        """
        none_return = tuple([None, None])

        if decoded_base64_authorization_header is None or not isinstance(decoded_base64_authorization_header, str):
            return none_return

        credentials = decoded_base64_authorization_header.split(':')
        if len(credentials) < 2:
            return none_return
        elif len(credentials) > 2:
            first_credential = credentials[0]
            second_credential = ':'.join(credentials[1:])

            return tuple([first_credential, second_credential])

        return tuple(credentials)

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Gets user by their credentials
        """
        if user_email and user_pwd and isinstance(user_email, str) and isinstance(user_pwd, str):
            users = User().search({'email': user_email})

            if users:
                for user in users:
                    if user.is_valid_password(user_pwd):
                        return user
                    else:
                        return None
            else:
                return None
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        My basic Basic Authentication
        """
        auth_header = self.authorization_header(request)
        encodedb64_h = self.extract_base64_authorization_header(auth_header)
        decodedb64_h = self.decode_base64_authorization_header(encodedb64_h)
        user_credentials = self.extract_user_credentials(decodedb64_h)

        return self.user_object_from_credentials(user_credentials[0], user_credentials[1])
