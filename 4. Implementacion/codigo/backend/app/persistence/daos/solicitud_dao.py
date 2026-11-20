from app.extensions import db
from app.persistence.models import Amistad, SolicitudAmistad, Usuario


class SolicitudDao:
    @staticmethod
    def get_by_id(solicitud_id: int) -> SolicitudAmistad | None:
        return db.session.get(SolicitudAmistad, solicitud_id)

    @staticmethod
    def existe_pendiente(emisor_id: int, receptor_id: int) -> bool:
        return (
            SolicitudAmistad.query.filter_by(
                emisor_id=emisor_id, receptor_id=receptor_id, estado="pendiente"
            ).first()
            is not None
        )

    @staticmethod
    def pendientes_para(usuario_id: int) -> list[SolicitudAmistad]:
        return (
            SolicitudAmistad.query.filter_by(receptor_id=usuario_id, estado="pendiente")
            .order_by(SolicitudAmistad.fecha_creacion.desc())
            .all()
        )

    @staticmethod
    def create(emisor_id: int, receptor_id: int) -> SolicitudAmistad:
        solicitud = SolicitudAmistad(emisor_id=emisor_id, receptor_id=receptor_id)
        db.session.add(solicitud)
        db.session.commit()
        return solicitud


class AmistadDao:
    @staticmethod
    def son_amigos(usuario1_id: int, usuario2_id: int) -> bool:
        a, b = sorted((usuario1_id, usuario2_id))
        return (
            Amistad.query.filter_by(usuario1_id=a, usuario2_id=b).first() is not None
        )

    @staticmethod
    def listar_amigos(usuario_id: int) -> list[Usuario]:
        amistades = Amistad.query.filter(
            db.or_(Amistad.usuario1_id == usuario_id, Amistad.usuario2_id == usuario_id)
        ).all()
        otros_ids = [
            a.usuario2_id if a.usuario1_id == usuario_id else a.usuario1_id
            for a in amistades
        ]
        if not otros_ids:
            return []
        return Usuario.query.filter(Usuario.id.in_(otros_ids)).all()
