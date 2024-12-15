from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "zxcced322kk0f4fFffF3FF333f"
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=999)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

    JWTManager(app)

    app.config.from_object('config.Config')

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.bp)

    return app
