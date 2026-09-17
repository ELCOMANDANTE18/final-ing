"""Regresión del bug de bypass de autenticación: check_password_hash tiene
que evaluarse ANTES de decidir la rama éxito/error, para cualquier
combinación de email inexistente / contraseña incorrecta."""

import pytest

from app.services.auth_service import (
    AuthService,
    CredencialesInvalidasError,
    EmailYaRegistradoError,
)


def test_login_con_contrasena_correcta_autentica(app, crear_usuario):
    with app.app_context():
        crear_usuario(email="ana@test.com", password="password123")

        usuario = AuthService.autenticar("ana@test.com", "password123")

        assert usuario.email == "ana@test.com"


def test_login_con_contrasena_incorrecta_no_autentica(app, crear_usuario):
    with app.app_context():
        crear_usuario(email="ana@test.com", password="password123")

        with pytest.raises(CredencialesInvalidasError):
            AuthService.autenticar("ana@test.com", "una-contrasena-cualquiera")


def test_login_con_email_inexistente_no_autentica(app):
    with app.app_context():
        with pytest.raises(CredencialesInvalidasError):
            AuthService.autenticar("no-existe@test.com", "lo-que-sea")


def test_registrar_con_email_duplicado_falla(app, crear_usuario):
    with app.app_context():
        crear_usuario(email="ana@test.com")

        with pytest.raises(EmailYaRegistradoError):
            AuthService.registrar("Ana de Nuevo", "ana@test.com", "password123")
