from flask import jsonify, request, current_app, abort
from flask.helpers import url_for
from sqlalchemy.exc import StatementError
from app import db
from app.api import bp
from app.models import Actor
from app.api.errors import not_found
from app.auth.auth import auth_required


@bp.route('/actors')
@auth_required('view:actors')
def get_actors():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit',
                             current_app.config['THECREW_OBJECTS_PER_PAGE'],
                             type=int)
    pagination = Actor.query.paginate(page, per_page=limit, error_out=False)

    result_dict = {
        'objects': [actor.to_json() for actor in pagination.items],
        'totalCount': pagination.total,
        'totalPages': pagination.pages,
        'page': pagination.page
    }
    if pagination.has_prev:
        result_dict['prevLink'] = url_for('api.get_actors',
                                          page=pagination.prev_num)
    if pagination.has_next:
        result_dict['nextLink'] = url_for('api.get_actors',
                                          page=pagination.next_num)

    return jsonify(result_dict)


@bp.route('actors/<string:actor_id>')
@auth_required('view:actors')
def get_actor(actor_id):
    actor = None
    try:
        actor = Actor.query.filter_by(uuid=actor_id).first_or_404()
    except StatementError:
        return not_found('please use the correct path parameter')
    return jsonify(actor.to_json())


@bp.route('/actors', methods=['POST'])
@auth_required('add:actors')
def create_actor():
    json_actor = request.json or {}
    actor = Actor.new_from_json(json_actor)
    db.session.commit()
    return jsonify(actor.to_json()), 201, \
        {'Location': url_for('api.get_actor', actor_id=str(actor.uuid))}


@bp.route('/actors/<string:actor_id>', methods=['PATCH'])
@auth_required('edit:actors')
def update_actor(actor_id):
    actor = None
    try:
        actor = Actor.query.filter_by(uuid=actor_id).first_or_404()
    except StatementError:
        return not_found('please use the correct path parameter')
    json_actor = request.json or {}
    actor.update_from_json(json_actor)
    db.session.commit()
    return jsonify(actor.to_json())


@bp.route('/actors/<string:actor_id>', methods=['DELETE'])
@auth_required('delete:actors')
def delete_actor(actor_id):
    actor = None
    try:
        actor = Actor.query.filter_by(uuid=actor_id).first_or_404()
    except StatementError:
        return not_found('please use the correct path parameter')
    db.session.delete(actor)
    db.session.commit()
    return '', 204
