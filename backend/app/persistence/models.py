from datetime import datetime, timezone

from sqlalchemy.orm import reconstructor

from app.extensions import db
from app.services.estados.estado_solicitud import Pendiente, estado_desde_nombre


def _now():
    return datetime.now(timezone.utc)


class Usuario(db.Model):
    """CU0001/CU0006. Además cumple el rol de Observable del patrón Observer
    (CU Notificar Solicitud Recibida): mantiene una lista de observadores
    en memoria (no persistida — no hace falta guardarla, se reconstruye
    igual en cada carga) y se la notifica a sí mismo cuando le pasa algo
    relevante, en vez de que el service llame al Notificador directo."""

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=_now)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_observadores()

    @reconstructor
    def _init_observadores(self):
        self._observadores = []
        # El Notificador (Singleton) está registrado como observador de
        # todo Usuario por defecto: es la única implementación de
        # Observador que existe en el sistema hoy.
        from app.services.notification_service import NotificationService

        self.agregar_observador(NotificationService.get_instance())

    def agregar_observador(self, observador) -> None:
        if observador not in self._observadores:
            self._observadores.append(observador)

    def eliminar_observador(self, observador) -> None:
        if observador in self._observadores:
            self._observadores.remove(observador)

    def notificar_observadores(self, evento: dict) -> None:
        for observador in self._observadores:
            observador.actualizar(evento)


class SolicitudAmistad(db.Model):
    """CU Solicitar Amistad / Aceptar-Rechazar Solicitud. Contexto del
    patrón State: `estado` persiste el nombre ("pendiente"/"aceptada"/
    "rechazada") y `_estado_obj` (no persistido) es el objeto State que
    resuelve las transiciones. aceptar()/rechazar() delegan siempre en
    `_estado_obj`, nunca deciden la transición ellas mismas."""

    __tablename__ = "solicitudes_amistad"
    __table_args__ = (
        db.UniqueConstraint("emisor_id", "receptor_id", name="uq_solicitud_par"),
    )

    id = db.Column(db.Integer, primary_key=True)
    emisor_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    receptor_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    estado = db.Column(db.String(20), nullable=False, default=Pendiente.nombre)
    fecha_creacion = db.Column(db.DateTime, default=_now)

    emisor = db.relationship("Usuario", foreign_keys=[emisor_id])
    receptor = db.relationship("Usuario", foreign_keys=[receptor_id])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.estado is None:
            self.estado = Pendiente.nombre
        self._init_estado_obj()

    @reconstructor
    def _init_estado_obj(self):
        self._estado_obj = estado_desde_nombre(self.estado)

    def set_estado(self, estado_obj) -> None:
        self._estado_obj = estado_obj
        self.estado = estado_obj.nombre

    def aceptar(self) -> None:
        self._estado_obj.aceptar(self)

    def rechazar(self) -> None:
        self._estado_obj.rechazar(self)

    def crear_vinculo_amistad(self) -> None:
        # Orden canónico (id menor primero) para que la UniqueConstraint y
        # AmistadDao.son_amigos() no dependan de quién fue emisor/receptor.
        u1, u2 = sorted((self.emisor_id, self.receptor_id))
        amistad = Amistad(usuario1_id=u1, usuario2_id=u2)
        db.session.add(amistad)


class Amistad(db.Model):
    """Vínculo de amistad ya confirmado. Se crea desde
    SolicitudAmistad.crear_vinculo_amistad(), en la misma transacción que
    el pasaje de estado a "aceptada" (ver AmistadService.responder_solicitud)."""

    __tablename__ = "amistades"
    __table_args__ = (
        db.UniqueConstraint("usuario1_id", "usuario2_id", name="uq_amistad_par"),
    )

    id = db.Column(db.Integer, primary_key=True)
    usuario1_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    usuario2_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=_now)
