from flask import redirect, render_template
from app.main import bp
from app.integrations.auth0 import build_authorize_url


@bp.route('/login', methods=['GET'])
@bp.route('/signup', methods=['GET'])
def login():
    return redirect(build_authorize_url())


@bp.route('/', methods=['GET'])
@bp.route('/welcome', methods=['GET'])
def welcome_callback():
    return render_template('welcome.html', title='TheCrew Casting Agency')
