#!/usr/bin/env python3
"""
logging module
"""
import re
import logging
from typing import List

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    obfusicate PII
    """
    for f in fields:
        message = re.sub(f"{f}=.*?{separator}", f"{f}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        sucure formatter
        """
        record.msg = filter_datum(self.fields, self.REDACTION, record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    creates a secure logger
    """
    custom_logger = logging.getLogger('test')
    custom_logger.setLevel('INFO')
    formatter = RedactingFormatter(PII_FIELDS)

    cns_handler = logging.StreamHandler()
    cns_handler.setLevel('INFO')
    cns_handler.setFormatter(formatter)

    custom_logger.addHandler(cns_handler)
    custom_logger.propagate = False

    return custom_logger()

