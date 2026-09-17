from datetime import datetime, timezone

from app.extensions import db


def _now():
    return datetime.now(timezone.utc)


class Usuario(db.Model):
    """CU0001 (Login) / CU0006 (Registrar Usuario)."""

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=_now)
