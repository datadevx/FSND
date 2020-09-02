from flask import jsonify, request
from app.auth import bp


@bp.route('/login/callback', methods=['GET'])
def login_callback():
    return jsonify({
        'query': {k: v
                  for k, v in request.args.items()},
        'headers': {k: v
                    for k, v in request.headers.items()}
    })
