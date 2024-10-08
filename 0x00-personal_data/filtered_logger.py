#!/usr/bin/env python3
"""
logging module
"""
import re
import logging
import os
from typing import List
from mysql.connector.connection import MySQLConnection

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

    return custom_logger

def get_db() -> MySQLConnection:
    """
    creates DB connector
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD')
    host = os.getenv('PERSONAL_DATA_DB_HOST')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    conn = MySQLConnection(
            host=host if host else 'localhost',
            user=user if user else 'root',
            passwd=password,
            db=db_name,
    )
    return conn

def main():
    """
    print protected user data from DB
    """

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    cols = [desc[0] for desc in cursor.description]
    f_info = []
    for row in cursor:
        kv_pairs = [f"{key}={val}" for key, val in zip(cols, row)]
        f_info.append(";".join(kv_pairs))

    logger = get_logger()

    for user_i in f_info:
        logger.info(user_i);

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
