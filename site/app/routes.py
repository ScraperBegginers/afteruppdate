from flask import Blueprint, request, jsonify

from .check_valid_data import verify_telegram_init_data
from .models import db, User, Tasks, Config, SubscribeChecker
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token, create_refresh_token
from dotenv import load_dotenv
import os
from time import time

load_dotenv() 

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
        return jsonify({'error': 'User not found'}), 400
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
@jwt_required()
def update_config():
    current_user = get_jwt_identity()
    admin_username = os.getenv("ADMIN_USERNAME")
    
    if current_user != admin_username:
        return jsonify({"error": "Доступ запрещен"}), 403
    
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

@bp.route('/api/token', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    admin_username = os.getenv("ADMIN_USERNAME")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if username == admin_username and password == admin_password:
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        }), 200
    else:
        return jsonify({"error": "Неправильные логин или пароль"}), 401

@bp.route('/api/spins/increment', methods=['POST'])
@jwt_required()
def increment_spins():
    current_user = get_jwt_identity()
    admin_username = os.getenv("ADMIN_USERNAME")
    
    if current_user != admin_username:
        return jsonify({"error": "Доступ запрещен"}), 403

    user_id = request.json.get("user_id")
    increment_by = request.json.get("increment_by", 1)

    user = User.query.filter_by(user_id=user_id).first()
    if user:
        user.spins += increment_by
        db.session.commit()
        return jsonify({"message": "Вращения обновлены", "total_spins": user.spins})
    return jsonify({"error": "Пользователь не найден"}), 404

@bp.route('/api/spins/decrement', methods=['POST'])
@jwt_required()
def decrement_spins():
    current_user = get_jwt_identity()
    admin_username = os.getenv("ADMIN_USERNAME")
    
    if current_user != admin_username:
        return jsonify({"error": "Доступ запрещен"}), 403

    user_id = request.json.get("user_id")
    decrement_by = request.json.get("increment_by", 1)

    user = User.query.filter_by(user_id=user_id).first()
    
    if user:
        if user.spins <= 0:
            return jsonify({"message": "У пользователя не осталось вращений!"}), 400
        user.spins -= decrement_by
        db.session.commit()
        return jsonify({"message": "Вращения обновлены", "total_spins": user.spins})
    return jsonify({"error": "Пользователь не найден"}), 404

@bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token)


@bp.route('/api/spins/newspin', methods=['POST'])
@jwt_required()
def newspin():
    current_user = get_jwt_identity()
    admin_username = os.getenv("ADMIN_USERNAME")
    
    if current_user != admin_username:
        return jsonify({"error": "Доступ запрещен"}), 403

    user_id = request.json.get("user_id")

    user = User.query.filter_by(user_id=user_id).first()
    
    if user:
        user.total_spins += 1
        db.session.commit()
        return jsonify({"message": "Колисество вращения обновлены", "total_spins": user.total_spins})
    return jsonify({"error": "Пользователь не найден"}), 404

@bp.route('/api/register_user', methods=['POST'])
@jwt_required()
def register_new_user():
    current_user = get_jwt_identity()
    admin_username = os.getenv("ADMIN_USERNAME")
    
    if current_user != admin_username:
        return jsonify({"error": "Доступ запрещен"}), 403

    user_id = request.json.get('user_id')
    first_name = request.json.get('firstname', "Unknown")
    username = request.json.get('username', "anonymous")

    new_user = User(
        user_id=user_id,
        firstname=first_name,
        username=username
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Пользователь создан'})

@bp.route('/api/update_daily_time', methods=['POST'])
@jwt_required()
def update_daily_time():
    current_user = get_jwt_identity()
    admin_username = os.getenv("ADMIN_USERNAME")
    
    if current_user != admin_username:
        return jsonify({"error": "Доступ запрещен"}), 403
    
    user_id = request.json.get('user_id')
    
    if not user_id:
        return jsonify({"error": "user_id не указан"}), 400
    
    user = User.query.filter_by(user_id=user_id).first()
    
    if user is None:
        return jsonify({"error": "Пользователь не найден"}), 404
    
    user.daily_spin = time()
    db.session.commit()
    
    return jsonify({"message": "Дата ежедневного приза была обновлена", "daily_time": user.daily_spin})

@bp.route('/api/subscription_trhrottling', methods=['POST'])
@jwt_required()
def input_throttling_subscription():
    current_user = get_jwt_identity()
    admin_username = os.getenv("ADMIN_USERNAME")
    
    if current_user != admin_username:
        return jsonify({"error": "Доступ запрещен"}), 403
    
    user_id = request.json.get("user_id")
    channel_id = request.json.get('channel_id')
    
    user = User.query.filter_by(user_id=user_id).first()
    
    if user is None:
        return jsonify({"error": "Пользователь не найден"}), 404
    
    new_check = SubscribeChecker(
        user_id=user_id,
        channel_id=channel_id
    )
    
    db.session.add(new_check)
    db.session.commit()
    
    return  jsonify({"message": "Троттлинг был добавлен в базу данных"})

@bp.route('/api/get_subscription_trhrottling', methods=['GET'])
def get_all_subscriptions():
    lists_throttlings = []

    user_id = request.args.get('user_id')

    if user_id:
        all_sub = SubscribeChecker.query.filter_by(user_id=user_id).all()
        if all_sub:
            lists_throttlings = [sub.to_dict() for sub in all_sub]
            return jsonify({"user_id": user_id, "subs": lists_throttlings})
        else:
            return jsonify({'error': "Пользователь не найден"}), 404

    all_subs = SubscribeChecker.query.all()
    lists_throttlings = [sub.to_dict() for sub in all_subs]

    return jsonify({"subs": lists_throttlings})

@bp.route('/api/set_refferal', methods=['POST'])
@jwt_required()
def set_referral():
    current_user = get_jwt_identity()
    admin_username = os.getenv("ADMIN_USERNAME")
    
    if current_user != admin_username:
        return jsonify({"error": "Доступ запрещен"}), 403
    
    referral = request.json.get('referral')
    user_id = request.json.get('user_id')
    
    if referral and user_id:
        get_user = User.query.filter_by(user_id=user_id).first()
        get_referral = User.query.filter_by(user_id=referral).first()
        
        if get_user and get_referral:
            if get_user.my_referral == 0:
                get_user.my_referral = referral
                db.session.commit()
                return jsonify({"message": f"Реферрал успешно добавлен к {user_id}"})
            else:
                return jsonify({'error': "У этого пользователя уже есть реферал!"}), 403
        else:
            return jsonify({'error': "Пользователь или реферал не найден в базе данных"}), 403
    
    return jsonify({"error": "Не указан user_id или referral"}), 403

@bp.route('/api/set_get_bonus', methods=['POST'])
@jwt_required()
def set_get_bonus_update():
    current_user = get_jwt_identity()
    admin_username = os.getenv("ADMIN_USERNAME")
    
    if current_user != admin_username:
        return jsonify({"error": "Доступ запрещен"}), 403
    
    user_id = request.json.get('user_id')
    
    if not user_id:
        return jsonify({"error": "Укажите user_id"}), 403
        
    user = User.query.filter_by(user_id=user_id).first()
    
    if not user:
        return jsonify({"error": "user_id указан не верно"}), 403

    if user.get_bonus_for_two_friends  == '1':
        return jsonify({"message": "У пользователя уже установлен статус True"})
    
    user.get_bonus_for_two_friends = '1'
    db.session.commit()
    return jsonify({"message": "Установлен статус True на бонусе"})
