"""Tests end-to-end vía el cliente de test de Flask (sin levantar el server
real) — mismo flujo que se probó a mano con curl al construir el proyecto."""

from conftest import auth_headers, login


def registrar(client, name, email, password="password123"):
    return client.post(
        "/auth/register", json={"name": name, "email": email, "password": password}
    )


def test_login_con_password_incorrecto_devuelve_401(client):
    registrar(client, "Ana", "ana@test.com")

    resp = client.post(
        "/auth/login", json={"email": "ana@test.com", "password": "incorrecta"}
    )

    assert resp.status_code == 401


def test_login_correcto_devuelve_token(client):
    registrar(client, "Ana", "ana@test.com")

    resp = client.post(
        "/auth/login", json={"email": "ana@test.com", "password": "password123"}
    )

    assert resp.status_code == 200
    assert "token" in resp.get_json()


def test_registro_duplicado_devuelve_409(client):
    registrar(client, "Ana", "ana@test.com")

    resp = registrar(client, "Ana", "ana@test.com")

    assert resp.status_code == 409


def test_flujo_completo_de_amistad_por_http(client):
    registrar(client, "Ana", "ana@test.com")
    registrar(client, "Beto", "beto@test.com")

    token_ana = login(client, "ana@test.com")
    token_beto = login(client, "beto@test.com")

    # Ana solicita amistad a Beto.
    resp = client.post(
        "/amistad/solicitudes",
        json={"email_receptor": "beto@test.com"},
        headers=auth_headers(token_ana),
    )
    assert resp.status_code == 201
    solicitud_id = resp.get_json()["id"]

    # Beto la ve en sus pendientes (== la "notificación" en la home).
    resp = client.get("/amistad/solicitudes/pendientes", headers=auth_headers(token_beto))
    assert resp.status_code == 200
    assert len(resp.get_json()) == 1

    # Ana no puede responder una solicitud que no le llegó a ella.
    resp = client.post(
        f"/amistad/solicitudes/{solicitud_id}/aceptar", headers=auth_headers(token_ana)
    )
    assert resp.status_code == 403

    # Beto acepta.
    resp = client.post(
        f"/amistad/solicitudes/{solicitud_id}/aceptar", headers=auth_headers(token_beto)
    )
    assert resp.status_code == 200
    assert resp.get_json()["estado"] == "aceptada"

    # Aceptar de nuevo la misma solicitud: transición inválida.
    resp = client.post(
        f"/amistad/solicitudes/{solicitud_id}/aceptar", headers=auth_headers(token_beto)
    )
    assert resp.status_code == 409

    # Ya son amigos, para los dos.
    resp = client.get("/amistad/amigos", headers=auth_headers(token_ana))
    assert [a["name"] for a in resp.get_json()] == ["Beto"]

    resp = client.get("/amistad/amigos", headers=auth_headers(token_beto))
    assert [a["name"] for a in resp.get_json()] == ["Ana"]


def test_solicitud_a_email_inexistente_devuelve_404(client):
    registrar(client, "Ana", "ana@test.com")
    token_ana = login(client, "ana@test.com")

    resp = client.post(
        "/amistad/solicitudes",
        json={"email_receptor": "no-existe@test.com"},
        headers=auth_headers(token_ana),
    )

    assert resp.status_code == 404


def test_endpoints_de_amistad_requieren_token(client):
    resp = client.get("/amistad/solicitudes/pendientes")
    assert resp.status_code == 401
