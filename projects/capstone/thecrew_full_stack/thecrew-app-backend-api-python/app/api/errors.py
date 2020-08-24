from flask import jsonify, request
from flask import json
from werkzeug.exceptions import HTTPException
from app.api import bp
from app.exceptions import ValidationsError


@bp.errorhandler(HTTPException)
def handle_http_exception(exception):
    response = exception.get_response()
    response.data = json.dumps({
        'message': exception.description,
        'status': exception.code,
        'path': request.path})
    response.content_type = 'application/json'
    return response


@bp.errorhandler(ValidationsError)
def handle_validation_error(exception):
    payload = {
        'errors': [{
            'field': e.field,
            'code': e.code,
            'description': e.description
        } for e in exception.errors],
        'message': exception.message,
        'status': 400,
        'path': request.path
    }
    response = jsonify(payload)
    response.status_code = 400
    return response

def not_found(message):
    return error_response(404, message)

def error_response(status_code, message):
    payload = {
        'message': message,
        'status': status_code,
        'path': request.path
    }
    response = jsonify(payload)
    response.status_code = status_code
    return response