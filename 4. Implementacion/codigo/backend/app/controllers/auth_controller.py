from flask import Blueprint, g, jsonify, request
from flask_jwt_extended import create_access_token
from marshmallow import Schema, ValidationError, fields, validate

from app.services.auth_service import (
    AuthService,
    CredencialesInvalidasError,
    EmailYaRegistradoError,
)
from app.utils.decorators import token_required

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


class RegisterSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    email = fields.Email(required=True)
    # "password segura" (imple.md CU0006): mínimo 8 caracteres.
    password = fields.Str(required=True, validate=validate.Length(min=8))


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=1))


@auth_bp.post("/register")
def register():
    try:
        data = RegisterSchema().load(request.get_json(silent=True) or {})
    except ValidationError:
        return jsonify({"error": "Por favor complete todos los campos correctamente."}), 400

    try:
        usuario = AuthService.registrar(**data)
    except EmailYaRegistradoError as exc:
        return jsonify({"error": str(exc)}), 409

    return jsonify({"id": usuario.id, "name": usuario.name, "email": usuario.email}), 201


@auth_bp.post("/login")
def login():
    try:
        data = LoginSchema().load(request.get_json(silent=True) or {})
    except ValidationError:
        return jsonify({"error": "Por favor complete todos los campos correctamente."}), 400

    try:
        usuario = AuthService.autenticar(**data)
    except CredencialesInvalidasError as exc:
        return jsonify({"error": str(exc)}), 401

    token = create_access_token(identity=str(usuario.id))
    return jsonify({"token": token, "user": {"id": usuario.id, "name": usuario.name}}), 200


@auth_bp.get("/me")
@token_required
def me():
    usuario = g.current_user
    return jsonify({"id": usuario.id, "name": usuario.name, "email": usuario.email}), 200
