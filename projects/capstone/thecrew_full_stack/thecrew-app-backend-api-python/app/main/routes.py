from flask import render_template
from app.main import bp


@bp.route('/welcome', methods=['GET'])
def welcome_callback():
    return render_template('welcome.html', title='TheCrew Casting Agency')
