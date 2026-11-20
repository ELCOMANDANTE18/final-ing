"""Unit tests del patrón State (estado_solicitud.py) en aislamiento total:
sin Flask, sin DB. El "contexto" es un doble de prueba que implementa lo
mínimo que el State necesita (duck typing), igual que SolicitudAmistad."""

import pytest

from app.services.estados.estado_solicitud import (
    Aceptada,
    EstadoInvalidoError,
    Pendiente,
    Rechazada,
    estado_desde_nombre,
)


class SolicitudFalsa:
    def __init__(self):
        self.estado = Pendiente.nombre
        self._estado_obj = Pendiente()
        self.vinculo_creado = False

    def set_estado(self, estado_obj):
        self._estado_obj = estado_obj
        self.estado = estado_obj.nombre

    def crear_vinculo_amistad(self):
        self.vinculo_creado = True

    def aceptar(self):
        self._estado_obj.aceptar(self)

    def rechazar(self):
        self._estado_obj.rechazar(self)


def test_pendiente_aceptar_crea_vinculo_y_pasa_a_aceptada():
    solicitud = SolicitudFalsa()

    solicitud.aceptar()

    assert solicitud.vinculo_creado is True
    assert solicitud.estado == Aceptada.nombre
    assert isinstance(solicitud._estado_obj, Aceptada)


def test_pendiente_rechazar_pasa_a_rechazada_sin_crear_vinculo():
    solicitud = SolicitudFalsa()

    solicitud.rechazar()

    assert solicitud.vinculo_creado is False
    assert solicitud.estado == Rechazada.nombre


def test_aceptada_no_admite_nuevas_transiciones():
    solicitud = SolicitudFalsa()
    solicitud.aceptar()

    with pytest.raises(EstadoInvalidoError):
        solicitud.aceptar()
    with pytest.raises(EstadoInvalidoError):
        solicitud.rechazar()

    # El estado no cambia ante una transición inválida.
    assert solicitud.estado == Aceptada.nombre


def test_rechazada_no_admite_nuevas_transiciones():
    solicitud = SolicitudFalsa()
    solicitud.rechazar()

    with pytest.raises(EstadoInvalidoError):
        solicitud.aceptar()
    with pytest.raises(EstadoInvalidoError):
        solicitud.rechazar()

    assert solicitud.estado == Rechazada.nombre


def test_estado_desde_nombre_reconstruye_el_objeto_correcto():
    assert isinstance(estado_desde_nombre("pendiente"), Pendiente)
    assert isinstance(estado_desde_nombre("aceptada"), Aceptada)
    assert isinstance(estado_desde_nombre("rechazada"), Rechazada)
