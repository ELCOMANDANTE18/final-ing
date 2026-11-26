import os

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config
from .utils.mail import MailConTimeout

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = MailConTimeout()

MIGRACIONES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'migrations')  # Flask-Mail con timeout SMTP (hallazgo H7)

# Claves que nunca deben firmar tokens: la que estaba fija en el código y la
# del archivo de ejemplo.
_CLAVES_INSEGURAS = {'super-secret', 'cambiar-por-un-valor-random-largo'}


def create_app(config_class=Config):
    app = Flask(__name__)

    # Configuración de la aplicación (antes se cargaba a mano acá, con la
    # clave JWT fija en el código; ahora sale de Config, que lee el .env).
    app.config.from_object(config_class)

    clave = app.config.get('JWT_SECRET_KEY')
    if not clave or clave in _CLAVES_INSEGURAS:
        raise RuntimeError(
            'Falta JWT_SECRET_KEY en backend/.env (o tiene un valor de ejemplo). '
            'Generar uno con: python -c "import secrets; print(secrets.token_hex(32))"'
        )

    # Inicializar extensiones
    db.init_app(app)
    # Carpeta fija: las migraciones se encuentran aunque el servidor se
    # arranque desde otra carpeta (hallazgo H11).
    migrate.init_app(app, db, directory=MIGRACIONES)
    jwt.init_app(app)
    mail.init_app(app)

    # Configurar CORS
    CORS(app, resources={r"/*": {"origins": app.config['CORS_ORIGIN']}})

    # Importar modelos para migraciones
    from .persistence import models  # noqa: F401

    # Registrar blueprints
    from .controllers.auth_controller import auth_bp
    from .controllers.invite_controller import invite_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(invite_bp, url_prefix='/invite')

    return app
