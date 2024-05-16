#!/usr/bin/env python3
"""
Regex-ing module
"""
import re
from typing import List


def filter_datum(fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """
    a function that returns a log message obfuscated
    """
    for field in fields:
        pattern = rf'{field}=([^;]*)'
        message = re.sub(pattern, f"{field}={redaction}", message)
    return message
