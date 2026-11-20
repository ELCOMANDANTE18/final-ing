"""Tests de integración (con DB real, sqlite de archivo temporal) del
service que orquesta el patrón State + dispara el Observer."""

import pytest

from app.persistence.daos.solicitud_dao import AmistadDao, SolicitudDao
from app.services.amistad_service import (
    AmistadService,
    NoAutorizadoError,
    SolicitudInvalidaError,
    SolicitudNoEncontradaError,
    UsuarioNoEncontradoError,
)
from app.services.estados.estado_solicitud import EstadoInvalidoError
from app.services.notification_service import NotificationService


def test_solicitar_amistad_crea_solicitud_pendiente_y_dispara_el_observer(
    app, crear_usuario, monkeypatch
):
    with app.app_context():
        emisor = crear_usuario(name="Ana", email="ana@test.com")
        receptor = crear_usuario(name="Beto", email="beto@test.com")

        eventos = []
        monkeypatch.setattr(
            NotificationService, "actualizar", lambda self, evento: eventos.append(evento)
        )

        solicitud = AmistadService.solicitar_amistad(emisor.id, "beto@test.com")

        assert solicitud.estado == "pendiente"
        assert solicitud.emisor_id == emisor.id
        assert solicitud.receptor_id == receptor.id
        # AmistadService nunca llama al Notificador directo: publica el
        # evento en el receptor y el Observer (NotificationService) es
        # quien reacciona. Si esto fuera una llamada directa, no habría
        # Observer, sería un service común.
        assert eventos == [
            {
                "tipo": "solicitud_recibida",
                "receptor_email": "beto@test.com",
                "emisor_nombre": "Ana",
            }
        ]


def test_no_se_puede_solicitar_amistad_a_uno_mismo(app, crear_usuario):
    with app.app_context():
        emisor = crear_usuario(name="Ana", email="ana@test.com")

        with pytest.raises(SolicitudInvalidaError):
            AmistadService.solicitar_amistad(emisor.id, "ana@test.com")


def test_no_se_puede_duplicar_una_solicitud_pendiente(app, crear_usuario):
    with app.app_context():
        emisor = crear_usuario(name="Ana", email="ana@test.com")
        crear_usuario(name="Beto", email="beto@test.com")

        AmistadService.solicitar_amistad(emisor.id, "beto@test.com")

        with pytest.raises(SolicitudInvalidaError):
            AmistadService.solicitar_amistad(emisor.id, "beto@test.com")


def test_receptor_inexistente_da_error(app, crear_usuario):
    with app.app_context():
        emisor = crear_usuario(name="Ana", email="ana@test.com")

        with pytest.raises(UsuarioNoEncontradoError):
            AmistadService.solicitar_amistad(emisor.id, "no-existe@test.com")


def test_aceptar_solicitud_crea_amistad_en_la_misma_transaccion(app, crear_usuario):
    with app.app_context():
        emisor = crear_usuario(name="Ana", email="ana@test.com")
        receptor = crear_usuario(name="Beto", email="beto@test.com")
        solicitud = AmistadService.solicitar_amistad(emisor.id, "beto@test.com")

        AmistadService.responder_solicitud(solicitud.id, usuario_id=receptor.id, aceptar=True)

        actualizada = SolicitudDao.get_by_id(solicitud.id)
        assert actualizada.estado == "aceptada"
        assert AmistadDao.son_amigos(emisor.id, receptor.id) is True


def test_no_se_puede_aceptar_dos_veces_la_misma_solicitud(app, crear_usuario):
    with app.app_context():
        emisor = crear_usuario(name="Ana", email="ana@test.com")
        receptor = crear_usuario(name="Beto", email="beto@test.com")
        solicitud = AmistadService.solicitar_amistad(emisor.id, "beto@test.com")

        AmistadService.responder_solicitud(solicitud.id, usuario_id=receptor.id, aceptar=True)

        with pytest.raises(EstadoInvalidoError):
            AmistadService.responder_solicitud(solicitud.id, usuario_id=receptor.id, aceptar=True)

        # El estado sigue en "aceptada": el intento inválido no lo corrompió.
        actualizada = SolicitudDao.get_by_id(solicitud.id)
        assert actualizada.estado == "aceptada"


def test_solo_el_receptor_puede_responder_la_solicitud(app, crear_usuario):
    with app.app_context():
        emisor = crear_usuario(name="Ana", email="ana@test.com")
        crear_usuario(name="Beto", email="beto@test.com")
        solicitud = AmistadService.solicitar_amistad(emisor.id, "beto@test.com")

        with pytest.raises(NoAutorizadoError):
            AmistadService.responder_solicitud(solicitud.id, usuario_id=emisor.id, aceptar=True)


def test_responder_solicitud_inexistente_da_error(app, crear_usuario):
    with app.app_context():
        usuario = crear_usuario(name="Ana", email="ana@test.com")

        with pytest.raises(SolicitudNoEncontradaError):
            AmistadService.responder_solicitud(999, usuario_id=usuario.id, aceptar=True)


def test_no_se_puede_solicitar_amistad_a_alguien_que_ya_es_amigo(app, crear_usuario):
    with app.app_context():
        emisor = crear_usuario(name="Ana", email="ana@test.com")
        receptor = crear_usuario(name="Beto", email="beto@test.com")
        solicitud = AmistadService.solicitar_amistad(emisor.id, "beto@test.com")
        AmistadService.responder_solicitud(solicitud.id, usuario_id=receptor.id, aceptar=True)

        with pytest.raises(SolicitudInvalidaError):
            AmistadService.solicitar_amistad(emisor.id, "beto@test.com")


def test_amigos_de_devuelve_solo_amistades_confirmadas(app, crear_usuario):
    with app.app_context():
        emisor = crear_usuario(name="Ana", email="ana@test.com")
        receptor = crear_usuario(name="Beto", email="beto@test.com")
        crear_usuario(name="Carla", email="carla@test.com")

        assert AmistadService.amigos_de(emisor.id) == []

        solicitud = AmistadService.solicitar_amistad(emisor.id, "beto@test.com")
        AmistadService.responder_solicitud(solicitud.id, usuario_id=receptor.id, aceptar=True)

        amigos = AmistadService.amigos_de(emisor.id)
        assert [a.email for a in amigos] == ["beto@test.com"]
