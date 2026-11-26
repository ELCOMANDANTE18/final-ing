"""Regresiones de los problemas de seguridad corregidos sobre el código
original del grupo, y el Singleton del notificador."""

import jwt as pyjwt
import pytest

from app import create_app
from app.config import Config, _env_bool
from app.services.notification_service import NotificationService


def test_un_token_firmado_con_la_clave_vieja_super_secret_no_sirve(app, client):
    """La clave estaba fija en el código ('super-secret'): con ella cualquiera
    podía fabricar un token válido. Ahora la firma sale del .env."""
    falso = pyjwt.encode(
        {'sub': '1', 'type': 'access', 'fresh': False, 'jti': 'x', 'nbf': 0, 'iat': 0, 'exp': 9999999999},
        'super-secret',
        algorithm='HS256',
    )
    resp = client.post('/invite', json={'email': 'beto@test.com'},
                       headers={'Authorization': f'Bearer {falso}'})
    assert resp.status_code == 401


@pytest.mark.parametrize('clave', [None, '', 'super-secret', 'cambiar-por-un-valor-random-largo'])
def test_la_aplicacion_no_arranca_sin_una_clave_jwt_segura(clave):
    class ConfigInsegura(Config):
        JWT_SECRET_KEY = clave

    with pytest.raises(RuntimeError, match='JWT_SECRET_KEY'):
        create_app(ConfigInsegura)


@pytest.mark.parametrize('valor', ['true', 'True', 'TRUE', '1'])
def test_mail_use_tls_acepta_true_en_minuscula(monkeypatch, valor):
    """Antes solo 'True' activaba TLS: con 'true' la clave de Gmail viajaba sin cifrar."""
    monkeypatch.setenv('MAIL_USE_TLS', valor)
    assert _env_bool('MAIL_USE_TLS') is True


def test_run_no_expone_el_depurador_en_la_red():
    """Antes: debug=True en host 0.0.0.0, que permite ejecutar código remoto."""
    from pathlib import Path

    lineas = (Path(__file__).resolve().parent.parent / 'run.py').read_text(encoding='utf-8').splitlines()
    # Solo el código: los comentarios explican el arreglo y citan los valores viejos.
    fuente = '\n'.join(l for l in lineas if not l.strip().startswith('#'))
    assert "host='127.0.0.1'" in fuente
    assert "'0.0.0.0'" not in fuente
    assert 'debug=True' not in fuente


def test_notification_service_es_singleton():
    assert NotificationService() is NotificationService()


# --- H11: el esquema sale de las migraciones ---

from contextlib import contextmanager


@contextmanager
def _app_con_base(ruta):
    """App con una base propia en `ruta`, dentro de su contexto. Al salir
    cierra la sesión y las conexiones (si no, quedan conexiones SQLite abiertas)."""
    from app import db

    class ConfigBase(Config):
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{ruta}'

    app = create_app(ConfigBase)
    with app.app_context():
        try:
            yield app
        finally:
            db.session.remove()
            db.engine.dispose()


def _tablas(app):
    from sqlalchemy import inspect
    from app import db
    return set(inspect(db.engine).get_table_names())


def _version(app):
    from sqlalchemy import text
    from app import db
    with db.engine.connect() as conexion:
        return conexion.execute(text('SELECT version_num FROM alembic_version')).scalar()


def test_las_migraciones_crean_el_mismo_esquema_que_los_modelos(tmp_path):
    """Una base nueva, armada solo con las migraciones, no difiere en nada de
    los modelos: ni tablas, ni columnas, ni índices."""
    from alembic.autogenerate import compare_metadata
    from alembic.migration import MigrationContext
    from app import db
    from app.persistence.migraciones import preparar_base

    with _app_con_base(tmp_path / 'nueva.db') as app:
        preparar_base()
        assert _tablas(app) == {'alembic_version', 'users', 'invitations'}
        with db.engine.connect() as conexion:
            assert compare_metadata(MigrationContext.configure(conexion), db.metadata) == []


def test_una_base_creada_con_create_all_se_adopta_sin_perder_datos(tmp_path):
    from app import db
    from app.persistence.daos.user_dao import UserDAO
    from app.persistence.migraciones import preparar_base

    with _app_con_base(tmp_path / 'vieja.db') as app:
        db.create_all()
        UserDAO.create('Ana', 'ana@test.com', 'hash')
        preparar_base()
        assert _version(app) == '0002_invitations'
        assert UserDAO.get_by_email('ana@test.com') is not None


def test_una_base_vieja_sin_invitaciones_recibe_la_tabla(tmp_path):
    """Base de antes de guardar las invitaciones (solo users): se marca como
    0001 y la migración 0002 agrega la tabla que falta."""
    from app import db
    from app.persistence.migraciones import preparar_base
    from app.persistence.models import User

    with _app_con_base(tmp_path / 'sin_invitaciones.db') as app:
        User.__table__.create(db.engine)
        preparar_base()
        assert 'invitations' in _tablas(app)
        assert _version(app) == '0002_invitations'


def test_run_usa_las_migraciones_y_no_create_all():
    from pathlib import Path
    lineas = (Path(__file__).resolve().parent.parent / 'run.py').read_text(encoding='utf-8').splitlines()
    fuente = '\n'.join(l for l in lineas if not l.strip().startswith('#'))
    assert 'preparar_base()' in fuente
    assert 'create_all' not in fuente
