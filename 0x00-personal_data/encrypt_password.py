#!/usr/bin/env python3
"""
password hasher module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    encrypts password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
