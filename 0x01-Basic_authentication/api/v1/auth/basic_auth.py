#!/usr/bin/env python3
"""
Basic Authentication mdule
"""
from api.v1.auth.auth import Auth
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
