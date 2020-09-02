from flask import jsonify, request
from werkzeug.http import HTTP_STATUS_CODES
from app.api import bp
from app.exceptions import ValidationsError
from app.auth.errors import AuthError


@bp.errorhandler(ValidationsError)
def handle_validation_error(error):
    errors = [{
        'field': e.field,
        'code': e.code,
        'description': e.description
    } for e in error.errors]
    return error_response(400, error.message, errors)


@bp.errorhandler(AuthError)
def handle_auth_error(error):
    errors = [{'code': error.code, 'description': error.description}]
    message = HTTP_STATUS_CODES.get(
        error.status_code) or 'Authentication failed'
    return error_response(error.status_code, message, errors)


def not_found(message):
    return error_response(404, message)


def handle_http_exception(exception):
    return error_response(exception.code, exception.description)


def error_response(status_code, message, errors=None):
    payload = {'message': message, 'status': status_code, 'path': request.path}
    if errors:
        payload['errors'] = errors
    response = jsonify(payload)
    response.status_code = status_code
    return response
