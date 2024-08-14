#!/usr/bin/env python3
"""
Auhentication module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Encrypts password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
