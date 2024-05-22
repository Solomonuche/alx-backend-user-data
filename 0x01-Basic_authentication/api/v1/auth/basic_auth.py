#!/usr/bin/env python3
"""
Basic authentication implementation
"""
from api.v1.auth.auth import Auth


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
