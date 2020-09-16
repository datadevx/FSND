from flask import jsonify, request, current_app
from flask.helpers import url_for
from sqlalchemy.exc import StatementError
from app import db, cache
from app.api import bp
from app.models import Movie
from app.api.errors import not_found
from app.auth.auth import auth_required
from app.integration.flask_caching import redis_is_not_available, delete_memoized


@bp.route('/movies')
@auth_required('view:movies')
@cache.memoize(unless=redis_is_not_available)
def get_movies():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit',
                             current_app.config['THECREW_OBJECTS_PER_PAGE'],
                             type=int)
    pagination = Movie.query.paginate(page, per_page=limit, error_out=False)

    result_dict = {
        'objects': [movie.to_json() for movie in pagination.items],
        'totalCount': pagination.total,
        'totalPages': pagination.pages,
        'page': pagination.page
    }
    if pagination.has_prev:
        result_dict['prevLink'] = url_for('api.get_movies',
                                          page=pagination.prev_num)
    if pagination.has_next:
        result_dict['nextLink'] = url_for('api.get_movies',
                                          page=pagination.next_num)

    return jsonify(result_dict)


@bp.route('movies/<string:movie_id>')
@auth_required('view:movies')
@cache.memoize(unless=redis_is_not_available)
def get_movie(movie_id):
    movie = None
    try:
        movie = Movie.query.filter_by(uuid=movie_id).first_or_404()
    except StatementError:
        return not_found('please use the correct path parameter')
    return jsonify(movie.to_json())


@bp.route('/movies', methods=['POST'])
@auth_required('add:movies')
def create_movie():
    json_movie = request.json or {}
    movie = Movie.new_from_json(json_movie)
    db.session.commit()
    delete_memoized(get_movies)
    return jsonify(movie.to_json()), 201, \
        {'Location': url_for('api.get_movie', movie_id=str(movie.uuid))}


@bp.route('/movies/<string:movie_id>', methods=['PATCH'])
@auth_required('edit:movies')
def update_movie(movie_id):
    movie = None
    try:
        movie = Movie.query.filter_by(uuid=movie_id).first_or_404()
    except StatementError:
        return not_found('please use the correct path parameter')
    json_movie = request.json or {}
    movie.update_from_json(json_movie)
    db.session.commit()
    delete_memoized(get_movies)
    delete_memoized(get_movie, movie_id)
    return jsonify(movie.to_json())


@bp.route('/movies/<string:movie_id>', methods=['DELETE'])
@auth_required('delete:movies')
def delete_movie(movie_id):
    movie = None
    try:
        movie = Movie.query.filter_by(uuid=movie_id).first_or_404()
    except StatementError:
        return not_found('please use the correct path parameter')
    db.session.delete(movie)
    db.session.commit()
    delete_memoized(get_movies)
    delete_memoized(get_movie, movie_id)
    return '', 204
