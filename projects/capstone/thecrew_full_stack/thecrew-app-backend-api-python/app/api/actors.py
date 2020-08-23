from flask import jsonify, request, current_app
from flask.helpers import url_for
from app import db
from app.api import bp
from app.models import Actor


@bp.route('/actors')
def get_actors():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', current_app.config[
        'THECREW_OBJECTS_PER_PAGE'], type=int)
    pagination = Actor.query.paginate(page, per_page=limit, error_out=False)

    result_dict = {'objects': [actor.to_json() for actor in pagination.items],
                   'totalCount': pagination.total,
                   'totalPages': pagination.pages,
                   'page': pagination.page}
    if pagination.has_prev:
        result_dict['prevLink'] = url_for(
            'api.get_actors', page=pagination.prev_num)
    if pagination.has_next:
        result_dict['nextLink'] = url_for(
            'api.get_actors', page=pagination.next_num)

    return jsonify(result_dict)


@bp.route('actors/<string:id>')
def get_actor(id):
    actor = Actor.query.filter_by(uuid=id).first_or_404()
    return jsonify(actor.to_json())


@bp.route('/actors', methods=['POST'])
def create_actor():
    actor = Actor.new_from_json(request.json)
    db.session.commit()
    return jsonify(actor.to_json()), 201, \
        {'Location': url_for('api.get_actor', id=actor.uuid)}


@bp.route('/actors/<string:id>', methods=['PATCH'])
def update_actor(id):
    actor = Actor.query.filter_by(uuid=id).first_or_404()
    actor.update_from_json(request.json)
    db.session.commit()
    return jsonify(actor.to_json())


@bp.route('/actors/<string:id>', methods=['DELETE'])
def delete_actor(id):
    actor = Actor.query.filter_by(uuid=id).first_or_404()
    db.session.delete(actor)
    db.session.commit()
    return '', 204
