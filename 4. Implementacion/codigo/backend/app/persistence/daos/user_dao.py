from ... import db
from ..models import User


def _normalizar(email):
    # Seguridad: sin esto, "ana@x.com" y "ANA@X.COM" eran dos cuentas distintas.
    return email.strip().lower()


class UserDAO:
    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=_normalizar(email)).first()

    @staticmethod
    def get_by_id(user_id):
        return db.session.get(User, user_id)

    @staticmethod
    def create(name, email, password_hash):
        user = User(name=name, email=_normalizar(email), password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user
