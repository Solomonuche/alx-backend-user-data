#!/usr/bin/env python3
"""
Regex-ing module
"""
import re
import logging
from typing import List

PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'ip')


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    a function that returns a log message obfuscated
    """
    for field in fields:
        pattern = rf'{field}=([^{separator}]*)'
        message = re.sub(pattern, f"{field}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ constructor
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        costume formatter
        """
        message = super().format(record)
        return filter_datum(self.fields,
                            self.REDACTION, message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    get logger function
    """

    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.propagate = False
    logger.addHandler(handler)

    return logger
