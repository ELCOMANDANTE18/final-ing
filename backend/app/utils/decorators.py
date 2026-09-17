from functools import wraps

from flask import g
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from app.persistence.daos.user_dao import UserDao


def token_required(fn):
    """Valida el JWT y deja el Usuario autenticado en `g.current_user`
    (endpoints existentes lo referencian como `current_user`, ver
    imple.md)."""

    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        g.current_user = UserDao.get_by_id(int(user_id))
        return fn(*args, **kwargs)

    return wrapper
