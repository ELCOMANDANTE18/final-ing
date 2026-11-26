from ..persistence.daos.invitation_dao import InvitationDAO
from ..persistence.models import Invitation
from .notification_service import NotificationService


class InvitationService:
    """CU0010: registra la invitación, pide el envío del correo y deja
    guardado el resultado (enviada o fallida)."""

    @staticmethod
    def invite(inviter, email):
        invitation = InvitationDAO.create(email=email, inviter_id=inviter.id)
        try:
            NotificationService().send_invitation(
                recipient_email=invitation.email, inviter_name=inviter.name)
        except Exception:
            # CU0010, ca 5.1: queda registrada como fallida y el error sube al
            # controller, que responde con un mensaje genérico.
            InvitationDAO.update_status(invitation, Invitation.FALLIDA)
            raise
        return InvitationDAO.update_status(invitation, Invitation.ENVIADA)
