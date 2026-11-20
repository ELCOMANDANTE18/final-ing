"""Datos semilla para probar el flujo de amistad end-to-end (login,
solicitudes pendientes para aceptar/rechazar, una ya rechazada y amistades
ya confirmadas) sin tener que crear todo a mano desde el frontend.

Inserta directamente contra los modelos (no pasa por AmistadService), así
que no dispara el Observer/NotificationService: no se manda ningún mail
real aunque `.env` tenga credenciales de Gmail configuradas.

Uso:
    cd backend && source venv/bin/activate
    python seed.py            # agrega los datos (falla si el email ya existe)
    python seed.py --reset    # borra usuarios/solicitudes/amistades antes de sembrar
"""

import argparse
from datetime import datetime, timedelta, timezone

from werkzeug.security import generate_password_hash

from app import create_app
from app.extensions import db
from app.persistence.models import Amistad, SolicitudAmistad, Usuario

PASSWORD = "hola123"

USUARIOS = [
    ("Victor Giménez", "victor@umbook.com"),
    ("Ana Torres", "ana@umbook.com"),
    ("Bruno Silva", "bruno@umbook.com"),
    ("Carla Núñez", "carla@umbook.com"),
    ("Diego Ramos", "diego@umbook.com"),
    ("Elena Vidal", "elena@umbook.com"),
    ("Franco Ibáñez", "franco@umbook.com"),
]


def _hace(minutos: int) -> datetime:
    return datetime.now(timezone.utc) - timedelta(minutes=minutos)


def _amistad(usuario1_id: int, usuario2_id: int, fecha_creacion: datetime) -> Amistad:
    u1, u2 = sorted((usuario1_id, usuario2_id))
    return Amistad(usuario1_id=u1, usuario2_id=u2, fecha_creacion=fecha_creacion)


def reset():
    SolicitudAmistad.query.delete()
    Amistad.query.delete()
    Usuario.query.delete()
    db.session.commit()


def seed():
    password_hash = generate_password_hash(PASSWORD)
    usuarios = {}
    for name, email in USUARIOS:
        u = Usuario(name=name, email=email, password_hash=password_hash)
        db.session.add(u)
        usuarios[email] = u
    db.session.flush()  # asigna ids sin cerrar la transacción

    v = usuarios["victor@umbook.com"]
    ana = usuarios["ana@umbook.com"]
    bruno = usuarios["bruno@umbook.com"]
    carla = usuarios["carla@umbook.com"]
    diego = usuarios["diego@umbook.com"]
    elena = usuarios["elena@umbook.com"]
    franco = usuarios["franco@umbook.com"]

    # --- Amistad ya confirmada: Ana <-> Victor -----------------------------
    db.session.add(
        SolicitudAmistad(
            emisor_id=ana.id,
            receptor_id=v.id,
            estado="aceptada",
            fecha_creacion=_hace(10080),  # hace una semana
        )
    )
    db.session.add(_amistad(ana.id, v.id, _hace(10079)))

    # --- Solicitud ya rechazada, para ver el historial ---------------------
    db.session.add(
        SolicitudAmistad(
            emisor_id=elena.id,
            receptor_id=v.id,
            estado="rechazada",
            fecha_creacion=_hace(4320),  # hace 3 días
        )
    )

    # --- Solicitudes pendientes recibidas por Victor: para aceptar/rechazar
    db.session.add(
        SolicitudAmistad(emisor_id=bruno.id, receptor_id=v.id, fecha_creacion=_hace(180))
    )
    db.session.add(
        SolicitudAmistad(emisor_id=carla.id, receptor_id=v.id, fecha_creacion=_hace(120))
    )
    db.session.add(
        SolicitudAmistad(emisor_id=diego.id, receptor_id=v.id, fecha_creacion=_hace(30))
    )

    # --- Solicitud enviada por Victor, todavía pendiente del lado de Franco
    db.session.add(
        SolicitudAmistad(emisor_id=v.id, receptor_id=franco.id, fecha_creacion=_hace(60))
    )

    # --- Amistad entre otros dos usuarios, sin relación con Victor ---------
    db.session.add(
        SolicitudAmistad(
            emisor_id=bruno.id,
            receptor_id=carla.id,
            estado="aceptada",
            fecha_creacion=_hace(20160),  # hace dos semanas
        )
    )
    db.session.add(_amistad(bruno.id, carla.id, _hace(20159)))

    db.session.commit()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Borra usuarios, solicitudes y amistades existentes antes de sembrar.",
    )
    args = parser.parse_args()

    app = create_app()
    with app.app_context():
        db.create_all()
        if args.reset:
            reset()
        seed()

    print(f"Listo. Password para todos los usuarios: {PASSWORD}\n")
    for name, email in USUARIOS:
        print(f"  {email:<22} {name}")
    print(
        "\nLogin sugerido para la demo: victor@umbook.com "
        f"/ {PASSWORD}"
        "\n  - 3 solicitudes pendientes para aceptar/rechazar (Bruno, Carla, Diego)"
        "\n  - 1 solicitud ya rechazada en el historial (Elena)"
        "\n  - 1 amigo ya confirmado (Ana)"
        "\n  - 1 solicitud propia todavía pendiente del otro lado (a Franco)"
    )


if __name__ == "__main__":
    main()
