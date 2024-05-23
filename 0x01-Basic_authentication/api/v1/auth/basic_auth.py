#!/usr/bin/env python3
"""
Basic authentication implementation
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    BasicAuth class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Basic - Base64 part
        """
        if not authorization_header or type(authorization_header) != str:
            return None
        if authorization_header.split()[0] != "Basic":
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        returns the decoded value of a Base64 string
        base64_authorization_header
        """
        if not base64_authorization_header or \
                type(base64_authorization_header) != str:
            return None
        try:
            return base64.b64decode(
                                    base64_authorization_header
                                    ).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """
        returns the user email and password from the Base64 decoded value
        """
        if not decoded_base64_authorization_header or \
                type(decoded_base64_authorization_header) != str:
            return None, None

        try:
            email, password = decoded_base64_authorization_header.split(":")
            return (email, password)
        except Exception:
            return None, None

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        returns the User instance based on his email and password.
        """
        if not user_email or type(user_email) != str:
            return None
        if not user_pwd or type(user_pwd) != str:
            return None
        if len(User.all()) == 0:
            return None

        user = User.search({"email": user_email})
        # the User search fuction returns a list
        if not user:
            return None
        if user[0].is_valid_password(user_pwd) is False:
            return None

        return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves the User instance for a request
        """
        auth = Auth()

        auth_header = auth.authorization_header(request)
        extract_header = self.extract_base64_authorization_header(auth_header)
        decoded_header = self.decode_base64_authorization_header(
                          extract_header
                          )
        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
