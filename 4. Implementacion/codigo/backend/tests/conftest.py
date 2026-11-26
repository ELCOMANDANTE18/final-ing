"""Configuración de las pruebas. Las variables de entorno se fijan ANTES de
importar `app`, porque Config las lee al cargarse; así las pruebas nunca usan
el .env real ni mandan correos."""

import os
import tempfile

_fd, _db_path = tempfile.mkstemp(suffix='.db')
os.environ['JWT_SECRET_KEY'] = 'clave-de-prueba-solo-para-tests-de-32-bytes-o-mas'
os.environ['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{_db_path}'
os.environ['MAIL_SUPPRESS_SEND'] = 'true'
os.environ['MAIL_USERNAME'] = 'umbook@test.com'
os.environ['MAIL_DEFAULT_SENDER'] = 'umbook@test.com'

import pytest  # noqa: E402

from app import create_app, db as _db  # noqa: E402


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


def registrar(client, name='Ana', email='ana@test.com', password='password123'):
    return client.post('/auth/register', json={'name': name, 'email': email, 'password': password})


def login(client, email='ana@test.com', password='password123'):
    return client.post('/auth/login', json={'email': email, 'password': password})


def token_de(client, email='ana@test.com', password='password123'):
    return login(client, email, password).get_json()['access_token']


def auth(token):
    return {'Authorization': f'Bearer {token}'}
