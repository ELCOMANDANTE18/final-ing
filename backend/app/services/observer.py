"""Interfaz Observador del patrón Observer. Vive separada de
notification_service.py para que persistence/models.py (Usuario, el
Observable) pueda depender solo de esta interfaz y no del singleton
concreto — evita un import circular models -> services -> models."""

from abc import ABC, abstractmethod


class Observador(ABC):
    @abstractmethod
    def actualizar(self, evento: dict) -> None: ...
