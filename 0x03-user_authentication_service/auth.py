#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hash password
    """
    passwd = password.encode('utf-8')
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(passwd, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a new user
        """
        user = None
        # check if a user exist
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            pass
        if user:
            raise ValueError(f'User {user.email} already exists')
        else:
            user = self._db.add_user(email, _hash_password(password))

        return user
