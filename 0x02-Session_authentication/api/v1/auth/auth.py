#!/usr/bin/env python3
"""
Authentication model
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth():
    """
    Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        authentication required
        """

        if not path or not excluded_paths:
            return True
        if path in excluded_paths or f"{path}/" in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Authorization header
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user request
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request
        """

        if request is None:
            return None

        session_name = getenv('SESSION_NAME', '_my_session_id')

        return request.cookies.get(session_name)
