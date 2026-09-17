from flask import Blueprint, g, jsonify, request
from marshmallow import Schema, ValidationError, fields

from app.services.amistad_service import (
    AmistadService,
    NoAutorizadoError,
    SolicitudInvalidaError,
    SolicitudNoEncontradaError,
    UsuarioNoEncontradoError,
)
from app.services.estados.estado_solicitud import EstadoInvalidoError
from app.utils.decorators import token_required

amistad_bp = Blueprint("amistad", __name__, url_prefix="/amistad")


class SolicitarAmistadSchema(Schema):
    email_receptor = fields.Email(required=True)


def _solicitud_a_dict(solicitud):
    return {
        "id": solicitud.id,
        "estado": solicitud.estado,
        "emisor": {"id": solicitud.emisor.id, "name": solicitud.emisor.name},
        "receptor": {"id": solicitud.receptor.id, "name": solicitud.receptor.name},
        "fecha_creacion": solicitud.fecha_creacion.isoformat(),
    }


@amistad_bp.post("/solicitudes")
@token_required
def solicitar_amistad():
    try:
        data = SolicitarAmistadSchema().load(request.get_json(silent=True) or {})
    except ValidationError:
        return jsonify({"error": "Por favor complete todos los campos correctamente."}), 400

    try:
        solicitud = AmistadService.solicitar_amistad(
            emisor_id=g.current_user.id, receptor_email=data["email_receptor"]
        )
    except UsuarioNoEncontradoError as exc:
        return jsonify({"error": str(exc)}), 404
    except SolicitudInvalidaError as exc:
        return jsonify({"error": str(exc)}), 409

    return jsonify(_solicitud_a_dict(solicitud)), 201


@amistad_bp.get("/solicitudes/pendientes")
@token_required
def solicitudes_pendientes():
    """Consulta derivada para la home ("notificaciones"): no hay una
    entidad Notificacion separada, la lista de solicitudes pendientes
    recibidas ES la notificación (ver PROMPT_CONSTRUCCION.md sección 5)."""
    pendientes = AmistadService.pendientes_para(g.current_user.id)
    return jsonify([_solicitud_a_dict(s) for s in pendientes]), 200


def _responder(solicitud_id: int, aceptar: bool):
    try:
        solicitud = AmistadService.responder_solicitud(
            solicitud_id=solicitud_id, usuario_id=g.current_user.id, aceptar=aceptar
        )
    except SolicitudNoEncontradaError as exc:
        return jsonify({"error": str(exc)}), 404
    except NoAutorizadoError as exc:
        return jsonify({"error": str(exc)}), 403
    except EstadoInvalidoError as exc:
        return jsonify({"error": str(exc)}), 409

    return jsonify(_solicitud_a_dict(solicitud)), 200


@amistad_bp.post("/solicitudes/<int:solicitud_id>/aceptar")
@token_required
def aceptar_solicitud(solicitud_id: int):
    return _responder(solicitud_id, aceptar=True)


@amistad_bp.post("/solicitudes/<int:solicitud_id>/rechazar")
@token_required
def rechazar_solicitud(solicitud_id: int):
    return _responder(solicitud_id, aceptar=False)
