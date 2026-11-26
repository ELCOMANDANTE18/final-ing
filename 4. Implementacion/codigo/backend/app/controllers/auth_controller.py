from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from marshmallow import Schema, ValidationError, fields, validate

from ..services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

# Mensajes de las fichas CU0001 y CU0006.
MSG_FORMULARIO = 'Por favor complete todos los campos correctamente.'
MSG_CREDENCIALES = 'Credenciales incorrectas.'
MSG_EMAIL_REGISTRADO = 'Este correo ya está registrado.'


class RegisterSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=128))
    email = fields.Email(required=True, validate=validate.Length(max=255))
    password = fields.Str(required=True, validate=validate.Length(min=8))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=1))


@auth_bp.route('/register', methods=['POST'])
def register():
    schema = RegisterSchema()
    try:
        data = schema.load(request.get_json(silent=True) or {})
    except ValidationError as err:
        return jsonify({'msg': MSG_FORMULARIO, 'errors': err.messages}), 400

    user = AuthService.register_user(data['name'], data['email'], data['password'])
    if user is None:
        # 409, como en el diagrama de secuencia de CU0006 (antes respondía 400).
        return jsonify({'msg': MSG_EMAIL_REGISTRADO}), 409

    return jsonify({'id': user.id, 'email': user.email}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    schema = LoginSchema()
    try:
        data = schema.load(request.get_json(silent=True) or {})
    except ValidationError:
        return jsonify({'msg': MSG_FORMULARIO}), 400

    user = AuthService.authenticate(data['email'], data['password'])
    if not user:
        # El mismo mensaje si el correo no existe o si la clave no coincide,
        # para no revelar qué correos están registrados (CU0001, ca 5.1).
        return jsonify({'msg': MSG_CREDENCIALES}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'access_token': access_token,
        'user': {'id': user.id, 'name': user.name, 'email': user.email},
    }), 200
