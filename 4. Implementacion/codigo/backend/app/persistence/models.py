from datetime import datetime, timezone

from .. import db


def _ahora():
    return datetime.now(timezone.utc)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=_ahora, nullable=False)


class Invitation(db.Model):
    """Invitación a la aplicación (CU0010). Se guarda antes de enviar el
    correo y su estado cambia según el resultado del envío:
    pendiente → enviada, o pendiente → fallida."""

    __tablename__ = 'invitations'

    PENDIENTE = 'pendiente'
    ENVIADA = 'enviada'
    FALLIDA = 'fallida'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), nullable=False, index=True)
    inviter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    status = db.Column(db.String(16), nullable=False, default=PENDIENTE)
    created_at = db.Column(db.DateTime, default=_ahora, nullable=False)

    inviter = db.relationship('User', backref=db.backref('invitations', lazy=True))
