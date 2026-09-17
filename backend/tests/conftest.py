"""Config de tests: variables de entorno seteadas ANTES de importar `app`
(app/config.py lee JWT_SECRET_KEY de os.environ al definir la clase Config,
así que tienen que existir antes del primer import)."""

import os
import tempfile

_db_fd, _db_path = tempfile.mkstemp(suffix=".db")
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-para-tests-32-bytes-o-mas")
os.environ.setdefault("SQLALCHEMY_DATABASE_URI", f"sqlite:///{_db_path}")
os.environ.setdefault("MAIL_SUPPRESS_SEND", "true")
os.environ.setdefault("MAIL_USERNAME", "test@example.com")
os.environ.setdefault("MAIL_DEFAULT_SENDER", "test@example.com")

import pytest  # noqa: E402  (después de setear el entorno a propósito)

from app import create_app  # noqa: E402
from app.extensions import db as _db  # noqa: E402
from app.persistence.daos.user_dao import UserDao  # noqa: E402
from werkzeug.security import generate_password_hash  # noqa: E402


@pytest.fixture()
def app():
    flask_app = create_app()
    flask_app.config.update(TESTING=True)

    with flask_app.app_context():
        _db.create_all()
        yield flask_app
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db(app):
    return _db


@pytest.fixture()
def crear_usuario(app):
    """Factory de usuarios de prueba, con password ya hasheado."""

    def _crear(name="Test", email="test@example.com", password="password123"):
        return UserDao.create(
            name=name, email=email, password_hash=generate_password_hash(password)
        )

    return _crear


def login(client, email, password="password123"):
    resp = client.post("/auth/login", json={"email": email, "password": password})
    return resp.get_json()["token"]


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}
