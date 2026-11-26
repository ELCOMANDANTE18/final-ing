from werkzeug.security import check_password_hash, generate_password_hash

from ..persistence.daos.user_dao import UserDAO


class AuthService:
    """CU0006 Registrar Usuario y CU0001 Iniciar Sesión.

    Los dos métodos siguen la misma convención: devuelven el `User` si la
    operación sale bien y `None` si no. Antes `register_user` devolvía una
    tupla `(User, mensaje)` cuyo mensaje nadie usaba (hallazgo H9)."""

    @staticmethod
    def register_user(name, email, password):
        """Crea la cuenta y devuelve el User, o None si el correo ya está
        registrado (también si otro registro simultáneo lo guardó primero)."""
        if UserDAO.get_by_email(email):
            return None
        return UserDAO.create(name=name, email=email, password_hash=generate_password_hash(password))

    @staticmethod
    def authenticate(email, password):
        """Devuelve el User si el correo existe y la contraseña coincide, o
        None en cualquier otro caso (el mismo resultado para los dos errores)."""
        user = UserDAO.get_by_email(email)
        if not user or not check_password_hash(user.password_hash, password):
            return None
        return user
