import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


from app import create_app, db
from app.models import Movie, Actor, Gender, movies_actors


app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Movie': Movie,
        'Actor': Actor,
        'Gender': Gender,
        'movies_actors': movies_actors
    }

if __name__ == "__main__":
    app.run(
        use_reloader=False,
        use_debugger=False,
        passthrough_errors=True,
        host='0.0.0.0'
    )