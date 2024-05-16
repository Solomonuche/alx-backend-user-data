#!/usr/bin/env python3
"""
Regex-ing module
"""
import re


def filter_datum(fields, redaction, message, separator):
    """
    a function that returns a log message obfuscated
    """

    for field in fields:
        pattern = rf'{field}=([^;]*)'
        message = re.sub(pattern, f"{field}={redaction}", message)
    return message
