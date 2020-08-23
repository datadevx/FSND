from datetime import datetime
from flask import current_app


def date_to_str(date):
    try:
        date_string = date.strftime(current_app.config['DATE_FORMAT'])
    except (TypeError, AttributeError):
        return None
    return date_string


def str_to_date(date_string):
    try:
        date = datetime.strptime(date_string, current_app.config[
            'DATE_FORMAT'])
    except ValueError:
        return None
    return date
