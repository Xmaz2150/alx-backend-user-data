#!/usr/bin/env python3
"""
Basic Authentication mdule
"""
from api.v1.auth.auth import Auth


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
