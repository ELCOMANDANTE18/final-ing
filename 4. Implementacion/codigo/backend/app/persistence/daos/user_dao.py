from sqlalchemy.exc import IntegrityError

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
        """Crea el usuario, o devuelve None si el correo ya está registrado.

        AuthService ya busca el correo antes de crear, pero dos registros
        simultáneos pueden pasar los dos esa búsqueda. En ese caso la
        restricción única de la base rechaza el segundo: se deshace la
        transacción y se devuelve None, en vez de dejar subir el error como
        un 500 (hallazgo H8)."""
        user = User(name=name, email=_normalizar(email), password_hash=password_hash)
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        return user
