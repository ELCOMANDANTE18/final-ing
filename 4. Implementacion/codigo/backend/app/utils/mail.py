"""Flask-Mail con timeout en la conexión SMTP.

Flask-Mail 0.9.1 abre la conexión con smtplib.SMTP(servidor, puerto), sin
timeout: si el servidor de correo no responde, la petición /invite queda
esperando indefinidamente (hallazgo H7 de DISEÑO_UMBook.md). Esta versión le
pasa MAIL_TIMEOUT segundos a smtplib, así cada operación de la conexión
(conectar, STARTTLS, login, envío) corta como máximo a ese tiempo y el error
sigue el camino del ca 5.1 de CU0010: la invitación queda fallida.
"""
import smtplib

from flask import current_app
from flask_mail import Connection, Mail


class _ConexionConTimeout(Connection):
    def configure_host(self):
        if self.mail.use_ssl:
            host = smtplib.SMTP_SSL(self.mail.server, self.mail.port, timeout=self.mail.timeout)
        else:
            host = smtplib.SMTP(self.mail.server, self.mail.port, timeout=self.mail.timeout)

        host.set_debuglevel(int(self.mail.debug))

        if self.mail.use_tls:
            host.starttls()
        if self.mail.username and self.mail.password:
            host.login(self.mail.username, self.mail.password)

        return host


class MailConTimeout(Mail):
    """Igual que flask_mail.Mail, pero sus conexiones usan MAIL_TIMEOUT."""

    def init_mail(self, config, debug=False, testing=False):
        estado = super().init_mail(config, debug, testing)
        estado.timeout = config.get('MAIL_TIMEOUT', 5)
        return estado

    def connect(self):
        app = getattr(self, 'app', None) or current_app
        try:
            return _ConexionConTimeout(app.extensions['mail'])
        except KeyError:
            raise RuntimeError('La aplicación no tiene configurado Flask-Mail')
