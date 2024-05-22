#!/usr/bin/env python3
"""
Basic authentication implementation
"""
from api.v1.auth.auth import Auth
import base64


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
