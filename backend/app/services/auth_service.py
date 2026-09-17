from werkzeug.security import check_password_hash, generate_password_hash

from app.persistence.daos.user_dao import UserDao


class CredencialesInvalidasError(Exception):
    """Usuario inexistente O contraseña incorrecta. Un solo mensaje genérico
    para ambos casos (no revelar si el email existe o no) — CU0001, curso
    alternativo "Credenciales incorrectas"."""


class EmailYaRegistradoError(Exception):
    pass


class AuthService:
    @staticmethod
    def registrar(name: str, email: str, password: str):
        if UserDao.get_by_email(email) is not None:
            raise EmailYaRegistradoError("Este correo ya está registrado.")
        password_hash = generate_password_hash(password)
        return UserDao.create(name=name, email=email, password_hash=password_hash)

    @staticmethod
    def autenticar(email: str, password: str):
        """Verifica la contraseña ANTES de decidir la rama de éxito/error.
        Bug corregido respecto al diagrama de secuencia original: ahí
        check_password_hash aparecía adentro de la rama "credenciales
        válidas", es decir después de haber elegido esa rama — cualquier
        email existente hubiera entrado sin importar la contraseña."""
        usuario = UserDao.get_by_email(email)
        if usuario is None or not check_password_hash(usuario.password_hash, password):
            raise CredencialesInvalidasError("Credenciales incorrectas.")
        return usuario
