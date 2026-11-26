from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from ..persistence.daos.user_dao import UserDAO


def token_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            identity = int(get_jwt_identity())
        except Exception:
            # Seguridad: antes se devolvía str(e), que le contaba al cliente por
            # qué falló la validación del token (firma, formato, vencimiento).
            return jsonify({'msg': 'Sesión inválida o vencida. Iniciá sesión de nuevo.'}), 401

        user = UserDAO.get_by_id(identity)
        if not user:
            return jsonify({'msg': 'Sesión inválida o vencida. Iniciá sesión de nuevo.'}), 401

        kwargs['current_user'] = user
        return fn(*args, **kwargs)
    return wrapper
