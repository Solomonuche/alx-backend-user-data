#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
from db import DB
from typing import Union
from user import User
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Hash password
    """
    passwd = password.encode('utf-8')
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(passwd, salt)


def _generate_uuid() -> str:
    """
    return a string representation of a new UUID. Use the uuid module.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a new user
        """
        if not email or not isinstance(email, str):
            raise None
        if not password or not isinstance(password, str):
            return None

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

    def valid_login(self, email: str, password: str) -> bool:
        """
        Credentials validation
        """
        if not email or not isinstance(email, str):
            raise False
        if not password or not isinstance(password, str):
            return False

        user = None
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            pass
        if user:
            passwd = password.encode('utf-8')
            return bcrypt.checkpw(passwd, user.hashed_password)
        return False

    def create_session(self, email: str) -> str:
        """
        returns the session ID as a string.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        Find user by session ID
        """
        if not session_id or not isinstance(session_id, str):
            return None
        user = None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroy session
        """
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None

        self._db.update_user(user.id, session_id=None)
        return None

    def get_reset_password_token(email: str) -> str:
        """
        Generate reset password token
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError
        if user:
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        raise ValueError
