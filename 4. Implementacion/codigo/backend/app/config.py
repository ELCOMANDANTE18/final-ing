import os

from dotenv import load_dotenv

# backend/.env, sin importar desde qué carpeta se arranque el servidor.
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, '.env'))


def _env_bool(nombre, por_defecto='false'):
    # Seguridad: antes se comparaba con 'True' (mayúscula), así que un .env con
    # MAIL_USE_TLS=true desactivaba TLS y la clave de Gmail viajaba sin cifrar.
    return os.getenv(nombre, por_defecto).strip().lower() in ('1', 'true', 'yes')


class Config:
    """Única fuente de configuración: create_app() lee todo de acá."""

    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///umbook.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Seguridad: antes estaba fija en el código ('super-secret'), y con ella
    # cualquiera podía firmar tokens válidos y entrar como cualquier usuario.
    # Ahora se lee de .env y create_app() se niega a arrancar sin ella.
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', '587'))
    MAIL_USE_TLS = _env_bool('MAIL_USE_TLS', 'true')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER') or os.getenv('MAIL_USERNAME')
    MAIL_SUPPRESS_SEND = _env_bool('MAIL_SUPPRESS_SEND')

    CORS_ORIGIN = os.getenv('CORS_ORIGIN', 'http://localhost:4200')
    # Dirección del frontend: arma el enlace de registro del correo de invitación.
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:4200')
