"""Tests del patrón Observer (Usuario Observable + NotificationService
Observador) y del Singleton."""

from app.persistence.models import Usuario
from app.services.notification_service import NotificationService


class ObservadorFalso:
    def __init__(self):
        self.eventos = []

    def actualizar(self, evento):
        self.eventos.append(evento)


def test_usuario_notifica_a_todos_sus_observadores_registrados(app):
    with app.app_context():
        usuario = Usuario(name="Ana", email="ana@test.com", password_hash="x")
        falso = ObservadorFalso()
        usuario.agregar_observador(falso)

        usuario.notificar_observadores({"tipo": "prueba"})

        assert {"tipo": "prueba"} in falso.eventos


def test_eliminar_observador_deja_de_recibir_eventos(app):
    with app.app_context():
        usuario = Usuario(name="Ana", email="ana@test.com", password_hash="x")
        falso = ObservadorFalso()
        usuario.agregar_observador(falso)
        usuario.eliminar_observador(falso)

        usuario.notificar_observadores({"tipo": "prueba"})

        assert falso.eventos == []


def test_notification_service_esta_registrado_como_observador_por_defecto(app):
    with app.app_context():
        usuario = Usuario(name="Ana", email="ana@test.com", password_hash="x")

        assert NotificationService.get_instance() in usuario._observadores


def test_notification_service_es_singleton():
    a = NotificationService.get_instance()
    b = NotificationService.get_instance()

    assert a is b


def test_actualizar_dispara_email_solo_para_solicitud_recibida(app, monkeypatch):
    with app.app_context():
        llamadas = []
        monkeypatch.setattr(
            NotificationService,
            "_enviar_email_plantilla",
            lambda self, **kwargs: llamadas.append(kwargs),
        )

        servicio = NotificationService.get_instance()
        servicio.actualizar({"tipo": "solicitud_recibida", "receptor_email": "b@test.com", "emisor_nombre": "Ana"})
        servicio.actualizar({"tipo": "otro_evento_no_manejado"})

        assert len(llamadas) == 1
        assert llamadas[0]["destinatario"] == "b@test.com"
        assert llamadas[0]["contexto"] == {"emisor_nombre": "Ana"}
