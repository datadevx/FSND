"""Utilities for using date objects.

    now(): the main function exported by this module.
"""

__author__ = "Filipe Bezerra de Sousa"

from datetime import datetime, timezone
from flask import current_app


def date_to_str(date):
    try:
        date_string = date.strftime(current_app.config['THECREW_DATE_FORMAT'])
    except (TypeError, AttributeError):
        return None
    return date_string


def str_to_date(date_string):
    try:
        date = datetime.strptime(
            date_string, current_app.config['THECREW_DATE_FORMAT'])
    except ValueError:
        return None
    return date


def now():
    return datetime.now(tz=timezone.utc)
