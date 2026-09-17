from app.extensions import db
from app.persistence.daos.solicitud_dao import AmistadDao, SolicitudDao
from app.persistence.daos.user_dao import UserDao
from app.services.estados.estado_solicitud import EstadoInvalidoError


class UsuarioNoEncontradoError(Exception):
    pass


class SolicitudInvalidaError(Exception):
    """Auto-solicitud, solicitud duplicada, o ya son amigos."""


class SolicitudNoEncontradaError(Exception):
    pass


class NoAutorizadoError(Exception):
    """El usuario autenticado no es el receptor de la solicitud que intenta
    responder — mismo principio de autorización que expuso el bug de
    AuthGuard: toda acción nueva se valida contra quién la pide."""


class AmistadService:
    @staticmethod
    def solicitar_amistad(emisor_id: int, receptor_email: str):
        emisor = UserDao.get_by_id(emisor_id)
        receptor = UserDao.get_by_email(receptor_email)

        if receptor is None:
            raise UsuarioNoEncontradoError("No existe un usuario con ese email.")
        if receptor.id == emisor.id:
            raise SolicitudInvalidaError("No podés enviarte una solicitud a vos mismo.")
        if AmistadDao.son_amigos(emisor.id, receptor.id):
            raise SolicitudInvalidaError("Ya son amigos.")
        if SolicitudDao.existe_pendiente(emisor.id, receptor.id):
            raise SolicitudInvalidaError("Ya existe una solicitud pendiente para este usuario.")

        solicitud = SolicitudDao.create(emisor_id=emisor.id, receptor_id=receptor.id)

        # Observer: el service NO llama al Notificador directo. Publica el
        # evento en el receptor (Observable) y quien esté suscripto
        # reacciona. Ver Usuario.notificar_observadores / NotificationService.actualizar.
        receptor.notificar_observadores(
            {
                "tipo": "solicitud_recibida",
                "receptor_email": receptor.email,
                "emisor_nombre": emisor.name,
            }
        )
        return solicitud

    @staticmethod
    def responder_solicitud(solicitud_id: int, usuario_id: int, aceptar: bool):
        solicitud = SolicitudDao.get_by_id(solicitud_id)
        if solicitud is None:
            raise SolicitudNoEncontradaError("La solicitud no existe.")
        if solicitud.receptor_id != usuario_id:
            raise NoAutorizadoError("Esta solicitud no te pertenece.")

        try:
            if aceptar:
                solicitud.aceptar()
            else:
                solicitud.rechazar()
            # Un solo commit para el cambio de estado y (si aceptó) el
            # vínculo de amistad: si algo de esto falla, rollback conjunto,
            # el estado no queda a mitad de camino en "aceptada".
            db.session.commit()
        except EstadoInvalidoError:
            db.session.rollback()
            raise
        except Exception:
            db.session.rollback()
            raise
        return solicitud

    @staticmethod
    def pendientes_para(usuario_id: int):
        return SolicitudDao.pendientes_para(usuario_id)
