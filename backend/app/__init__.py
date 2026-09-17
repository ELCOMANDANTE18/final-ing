from flask import Flask

from app.config import Config
from app.extensions import cors, db, jwt, mail, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": app.config["CORS_ORIGIN"]}})

    from app.services.notification_service import NotificationService

    NotificationService.get_instance().init_app(mail)

    from app.controllers.auth_controller import auth_bp
    from app.controllers.amistad_controller import amistad_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(amistad_bp)

    return app
