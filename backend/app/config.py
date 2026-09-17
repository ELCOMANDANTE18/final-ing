import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    """Fuente única de configuración. create_app() SIEMPRE lee de acá,
    nunca hardcodea valores propios (deuda corregida respecto a la primera
    versión del proyecto, ver tareas.md Fase 1)."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI",
        "sqlite:///" + os.path.join(basedir, "instance", "umbook.db"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", MAIL_USERNAME)
    MAIL_SUPPRESS_SEND = os.environ.get("MAIL_SUPPRESS_SEND", "false").lower() == "true"

    CORS_ORIGIN = os.environ.get("CORS_ORIGIN", "http://localhost:4200")
