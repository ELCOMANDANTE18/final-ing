from flask import Blueprint, current_app, jsonify, request
from marshmallow import Schema, ValidationError, fields, validate

from ..services.invitation_service import InvitationService
from ..utils.decorators import token_required

invite_bp = Blueprint('invite', __name__)


class InviteSchema(Schema):
    # rnf 2.1 de CU0010: formato RFC 5322, máximo 254 caracteres.
    email = fields.Email(required=True, validate=validate.Length(max=254))


@invite_bp.route('', methods=['POST'])
@token_required
def invite(current_user):
    schema = InviteSchema()
    try:
        data = schema.load(request.get_json(silent=True) or {})
    except ValidationError as err:
        return jsonify({'msg': 'Ingresá un correo válido.', 'errors': err.messages}), 400

    try:
        InvitationService.invite(inviter=current_user, email=data['email'])
    except Exception:
        # Seguridad: antes se devolvía str(e) al cliente, con detalles del
        # servidor de correo. Ahora el detalle queda solo en el log.
        current_app.logger.exception('No se pudo enviar la invitación a %s', data['email'])
        return jsonify({'msg': 'No se pudo enviar la invitación. Intentá de nuevo.'}), 500

    return jsonify({'msg': 'Invitación enviada.'}), 200
