"""Patrón State para SolicitudAmistad (CU Solicitar Amistad / Aceptar-Rechazar
Solicitud). Cada estado decide qué transiciones son válidas; SolicitudAmistad
(el "contexto" del patrón) delega en el estado actual y nunca implementa la
lógica de transición ella misma.

No importa `SolicitudAmistad` a propósito: el estado opera sobre el contexto
por duck typing (necesita `.set_estado()` y `.crear_vinculo_amistad()`), lo
que evita un import circular entre persistence.models y este módulo.
"""

from abc import ABC, abstractmethod


class EstadoInvalidoError(Exception):
    """Se pidió una transición que el estado actual no permite."""


class EstadoSolicitud(ABC):
    nombre: str

    @abstractmethod
    def aceptar(self, solicitud) -> None: ...

    @abstractmethod
    def rechazar(self, solicitud) -> None: ...


class Pendiente(EstadoSolicitud):
    nombre = "pendiente"

    def aceptar(self, solicitud) -> None:
        # Mismo commit/transacción que el cambio de estado (ver AmistadService):
        # si crear_vinculo_amistad() falla, set_estado() tampoco debe persistirse.
        solicitud.crear_vinculo_amistad()
        solicitud.set_estado(Aceptada())

    def rechazar(self, solicitud) -> None:
        solicitud.set_estado(Rechazada())


class Aceptada(EstadoSolicitud):
    nombre = "aceptada"

    def aceptar(self, solicitud) -> None:
        raise EstadoInvalidoError("La solicitud ya fue aceptada.")

    def rechazar(self, solicitud) -> None:
        raise EstadoInvalidoError("La solicitud ya fue aceptada, no se puede rechazar.")


class Rechazada(EstadoSolicitud):
    nombre = "rechazada"

    def aceptar(self, solicitud) -> None:
        raise EstadoInvalidoError("La solicitud ya fue rechazada, no se puede aceptar.")

    def rechazar(self, solicitud) -> None:
        raise EstadoInvalidoError("La solicitud ya fue rechazada.")


ESTADOS_POR_NOMBRE = {
    Pendiente.nombre: Pendiente,
    Aceptada.nombre: Aceptada,
    Rechazada.nombre: Rechazada,
}


def estado_desde_nombre(nombre: str) -> EstadoSolicitud:
    return ESTADOS_POR_NOMBRE[nombre]()
