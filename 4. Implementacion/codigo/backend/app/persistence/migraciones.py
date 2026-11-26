"""Lleva la base de datos a la última migración (hallazgo H11).

Antes, run.py creaba las tablas con db.create_all(), que crea las que faltan
pero no modifica las existentes: cambiar una columna obligaba a borrar la
base. Ahora el esquema sale de las migraciones de Alembic (migrations/).

Una base creada antes con create_all() no tiene la tabla alembic_version.
Para no perder sus datos se marca con la migración que ya tiene aplicada
(solo users -> 0001_users; users e invitations -> 0002_invitations) y
después se aplican las que falten.
"""
from flask_migrate import stamp, upgrade
from sqlalchemy import inspect

from .. import db


def preparar_base():
    tablas = set(inspect(db.engine).get_table_names())
    if 'alembic_version' not in tablas and 'users' in tablas:
        stamp(revision='0002_invitations' if 'invitations' in tablas else '0001_users')
    upgrade()
