from app.extensions import db
from app.persistence.models import Usuario


class UserDao:
    @staticmethod
    def get_by_email(email: str) -> Usuario | None:
        return Usuario.query.filter_by(email=email).first()

    @staticmethod
    def get_by_id(user_id: int) -> Usuario | None:
        return Usuario.query.get(user_id)

    @staticmethod
    def create(name: str, email: str, password_hash: str) -> Usuario:
        usuario = Usuario(name=name, email=email, password_hash=password_hash)
        db.session.add(usuario)
        db.session.commit()
        return usuario
