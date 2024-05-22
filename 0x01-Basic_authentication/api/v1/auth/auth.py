#!/usr/bin/env python3
"""
Authentication model
"""
from flask import request


class Auth():
    """
    Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        authentication required
        """

        return False

    def authorization_header(self, request=None) -> str:
        """
        Authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user request
        """
        return None
