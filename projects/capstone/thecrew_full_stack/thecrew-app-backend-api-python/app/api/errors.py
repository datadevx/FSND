from flask import jsonify, request
from app.api import bp
from app.exceptions import ValidationsError


@bp.errorhandler(ValidationsError)
def handle_validation_error(exception):
    errors = [{'field': e.field, 'code': e.code, 'description': e.description
               } for e in exception.errors]
    return error_response(400, exception.message, errors)


def not_found(message):
    return error_response(404, message)


def handle_http_exception(exception):
    return error_response(exception.code, exception.description)


def error_response(status_code, message, errors=None):
    payload = {
        'message': message,
        'status': status_code,
        'path': request.path
    }
    if errors:
        payload['errors'] = errors
    response = jsonify(payload)
    response.status_code = status_code
    return response
