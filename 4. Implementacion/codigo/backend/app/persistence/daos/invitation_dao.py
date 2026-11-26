from ... import db
from ..models import Invitation


class InvitationDAO:
    @staticmethod
    def create(email, inviter_id):
        invitation = Invitation(
            email=email.strip().lower(),
            inviter_id=inviter_id,
            status=Invitation.PENDIENTE,
        )
        db.session.add(invitation)
        db.session.commit()
        return invitation

    @staticmethod
    def update_status(invitation, status):
        invitation.status = status
        db.session.commit()
        return invitation

    @staticmethod
    def list_by_inviter(inviter_id):
        return (Invitation.query.filter_by(inviter_id=inviter_id)
                .order_by(Invitation.created_at.desc()).all())
