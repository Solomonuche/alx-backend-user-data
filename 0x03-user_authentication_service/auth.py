#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash password
    """
    passwd = password.encode('utf-8')
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(passwd, salt)
