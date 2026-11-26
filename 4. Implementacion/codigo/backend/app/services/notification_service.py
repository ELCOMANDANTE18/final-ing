import threading

from flask import current_app
from flask_mail import Message

from .. import mail


class NotificationService:
    """Singleton (doble verificación con candado): una sola instancia envía
    todos los correos de la aplicación."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def send_invitation(self, recipient_email, inviter_name):
        subject = '¡Te invitaron a UMBook!'
        # Enlace a la pantalla de registro (CU0006), como dice CU0010.
        register_url = f"{current_app.config['FRONTEND_URL'].rstrip('/')}/register"
        body = (
            f'Hola, {inviter_name} te invitó a sumarte a UMBook.\n\n'
            f'Para crear tu cuenta, entrá a este enlace: {register_url}'
        )
        msg = Message(
            subject=subject,
            recipients=[recipient_email],
            body=body,
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
        )
        # Si el envío falla, la excepción sube al controller, que la registra
        # en el log y responde con un mensaje genérico (CU0010, ca 5.1).
        mail.send(msg)
        current_app.logger.info('Invitación enviada a %s', recipient_email)
