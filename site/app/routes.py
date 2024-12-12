from flask import Blueprint, request, jsonify

from .check_valid_data import verify_telegram_init_data
from .models import db, User, Tasks, Config

bp = Blueprint('routes', __name__)

@bp.route('/api/verify-init-data', methods=['POST'])
def verify_init_data():
    data = request.json
    init_data = data.get('initData')

    if not init_data:
        return jsonify({'error': 'No initData provided'}), 400

    is_valid = verify_telegram_init_data(init_data=init_data, bot_token='5544856701:AAGsqlJQnBuDjN3wmF4wK2LHrIkK6sPLCew')
    if is_valid:
        return jsonify({'message': 'InitData is valid'}), 200
    else:
        return jsonify({'message': 'InitData is not invalid'}), 400

@bp.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())

@bp.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Tasks.query.all()
    tasks_list = [task.to_dict() for task in tasks]

    return jsonify(tasks_list)

@bp.route('/api/user/get_friends/<int:user_id>', methods=['GET'])
def get_friends(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    total_friends = User.query.filter_by(my_referral=user_id).count()

    return jsonify({'total_friends': total_friends})

@bp.route('/api/config', methods=['GET'])
def get_config():
    config = Config.query.first()
    if not config:
        return jsonify({'error': 'Configuration not found'}), 404
    return jsonify(config.to_dict())

@bp.route('/api/config', methods=['POST'])
def update_config():
    data = request.json
    config = Config.query.first()
    if not config:
        config = Config()
        db.session.add(config)

    if 'link_manager' in data:
        config.link_manager = data['link_manager']
    if 'link_partner' in data:
        config.link_partner = data['link_partner']
    if 'link_gift' in data:
        config.link_gift = data['link_gift']

    db.session.commit()
    return jsonify({'message': 'Configuration updated successfully'})
