from flask import Blueprint


bp = Blueprint('api', __name__)


@bp.after_app_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Headers', 'Content-Type: Authorization'
    )
    response.headers.add(
        'Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS'
    )
    return response


from app.api import actors