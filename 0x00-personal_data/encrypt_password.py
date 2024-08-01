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

def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    password validator
    """
    new_hash = bcrypt.hashpw(password.encode(),  hashed_password)
    return new_hash == hashed_password
