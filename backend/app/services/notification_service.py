import threading

from flask_mail import Message

from app.services.observer import Observador


class NotificationService(Observador):
    """Singleton (double-checked locking) + Observador. Ya existía como
    Singleton puro (envío de invitaciones, CU0010); acá se le suma la
    interfaz Observador para que también reaccione a eventos de otros
    Observable (Usuario) sin que el service que dispara el evento conozca
    al Notificador."""

    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        if NotificationService._instance is not None:
            raise RuntimeError("Usar NotificationService.get_instance(), no el constructor.")
        self._mail = None

    @staticmethod
    def get_instance() -> "NotificationService":
        if NotificationService._instance is None:
            with NotificationService._lock:
                if NotificationService._instance is None:
                    NotificationService._instance = NotificationService()
        return NotificationService._instance

    def init_app(self, mail) -> None:
        self._mail = mail

    # --- Observador ---
    def actualizar(self, evento: dict) -> None:
        """Reacciona a eventos publicados por notificar_observadores() de
        un Usuario. Hoy el único evento que dispara acción es
        "solicitud_recibida" (CU Notificar Solicitud de Amistad Recibida)."""
        if evento.get("tipo") == "solicitud_recibida":
            destinatario = evento["receptor_email"]
            mensaje = (
                f"{evento['emisor_nombre']} te envió una solicitud de amistad en UMBook."
            )
            self.enviar_email(destinatario, mensaje)

    # --- API preexistente (CU0010), no se le cambia la firma ---
    def enviar_email(self, destinatario: str, mensaje: str) -> None:
        if self._mail is None:
            raise RuntimeError("NotificationService no inicializado: falta init_app(mail).")
        msg = Message(subject="UMBook", recipients=[destinatario], body=mensaje)
        self._mail.send(msg)

    def notificar(self, evento: dict) -> None:
        self.actualizar(evento)
