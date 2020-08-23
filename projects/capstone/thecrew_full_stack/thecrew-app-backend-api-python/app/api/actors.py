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

    actors = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_actors', page=pagination.prev_num)
    next = None
    if pagination.has_next:
        next = url_for('api.get_actors', page=pagination.next_num)

    #TODO: Fix prev and next returning None, they need to be removed from
    # the response
    #TODO: rename movies and standardize it to objects Naming
    #TODO: rename count and standardize it to objects totalCount
    #TODO: include page
    #TODO: include totalPages
    return jsonify({
        'actors': [actor.to_json() for actor in actors],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@bp.route('actors/<string:id>')
def get_actor(id):
    actor = Actor.query.filter_by(uuid=id).first_or_404()
    return jsonify(actor.to_json())


@bp.route('/actors', methods=['POST'])
def new_actor():
    actor = Actor.from_json(request.json)
    db.session.commit()
    return jsonify(actor.to_json()), 201, \
        {'Location': url_for('api.get_actor', id=actor.uuid)}


@bp.route('/actors/<string:id>', methods=['PATCH'])
def edit_actor(id):
    actor = Actor.query.filter_by(uuid=id).first_or_404()
    json_actor = request.json

    for k, v in json_actor.items():
        setattr(actor, k, v)

    return jsonify(actor.to_json())


@bp.route('/actors/<string:id>', methods=['DELETE'])
def delete_actor(id):
    actor = Actor.query.filter_by(uuid=id).first_or_404()
    db.session.delete(actor)
    db.session.commit()
    return '', 204
