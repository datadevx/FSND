from flask import jsonify, request, current_app
from flask.helpers import url_for
from app import db
from app.api import bp
from app.models import Movie


@bp.route('/movies')
def get_movies():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', current_app.config[
        'THECREW_OBJECTS_PER_PAGE'], type=int)
    pagination = Movie.query.paginate(page, per_page=limit, error_out=False)

    result_dict = {'objects': [movie.to_json() for movie in pagination.items],
                   'totalCount': pagination.total,
                   'totalPages': pagination.pages,
                   'page': pagination.page}
    if pagination.has_prev:
        result_dict['prevLink'] = url_for(
            'api.get_movies', page=pagination.prev_num)
    if pagination.has_next:
        result_dict['nextLink'] = url_for(
            'api.get_movies', page=pagination.next_num)

    return jsonify(result_dict)


@bp.route('movies/<string:id>')
def get_movie(id):
    movie = Movie.query.filter_by(uuid=id).first_or_404()
    return jsonify(movie.to_json())


@bp.route('/movies', methods=['POST'])
def create_movie():
    movie = Movie.new_from_json(request.json)
    db.session.commit()
    return jsonify(movie.to_json()), 201, \
        {'Location': url_for('api.get_movie', id=str(movie.uuid))}


@bp.route('/movies/<string:id>', methods=['PATCH'])
def update_movie(id):
    movie = Movie.query.filter_by(uuid=id).first_or_404()
    movie.update_from_json(request.json)
    db.session.commit()
    return jsonify(movie.to_json())


@bp.route('/movies/<string:id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.query.filter_by(uuid=id).first_or_404()
    db.session.delete(movie)
    db.session.commit()
    return '', 204
