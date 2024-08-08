#!/usr/bin/env python3
"""
Session Authentication mdule
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    Session Authentication class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates session
        """
        if user_id and isinstance(user_id, str):
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id

            return session_id
