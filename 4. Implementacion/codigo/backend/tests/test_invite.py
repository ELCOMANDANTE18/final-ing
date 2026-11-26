"""CU0010 Invitación a la aplicación, a través de la API."""

from datetime import timedelta

from conftest import auth, registrar, token_de
from flask_jwt_extended import create_access_token

from app import mail
from app.persistence.models import Invitation


def test_invitacion_exitosa_envia_un_correo_al_invitado(app, client):
    registrar(client, name='Ana')
    token = token_de(client)

    with mail.record_messages() as enviados:
        resp = client.post('/invite', json={'email': 'beto@test.com'}, headers=auth(token))

    assert resp.status_code == 200
    assert resp.get_json() == {'msg': 'Invitación enviada.'}
    assert len(enviados) == 1
    assert enviados[0].recipients == ['beto@test.com']
    assert 'Ana' in enviados[0].body


def test_invitar_sin_token_devuelve_401(client):
    resp = client.post('/invite', json={'email': 'beto@test.com'})
    assert resp.status_code == 401


def test_correo_invalido_devuelve_400_y_no_envia_nada(client):
    registrar(client)
    token = token_de(client)
    with mail.record_messages() as enviados:
        resp = client.post('/invite', json={'email': 'esto-no-es-un-correo'}, headers=auth(token))
    assert resp.status_code == 400
    assert enviados == []


def test_correo_de_mas_de_254_caracteres_devuelve_400(client):
    """rnf 2.1 de CU0010: máximo 254 caracteres."""
    registrar(client)
    token = token_de(client)
    largo = 'a' * 64 + '@' + ('b' * 60 + '.') * 4 + 'com'
    assert len(largo) > 254
    resp = client.post('/invite', json={'email': largo}, headers=auth(token))
    assert resp.status_code == 400


def test_falla_del_correo_responde_500_sin_detalles_internos(app, client, monkeypatch):
    """CU0010 ca 5.1: se avisa del fallo. El detalle del servidor de correo
    queda en el log y no se le devuelve al cliente."""
    registrar(client)
    token = token_de(client)

    def smtp_caido(msg):
        raise ConnectionError('smtp.gmail.com:587 rechazó la autenticación de umbook@test.com')

    monkeypatch.setattr(mail, 'send', smtp_caido)
    resp = client.post('/invite', json={'email': 'beto@test.com'}, headers=auth(token))

    assert resp.status_code == 500
    assert resp.get_json() == {'msg': 'No se pudo enviar la invitación. Intentá de nuevo.'}
    assert 'smtp' not in resp.get_data(as_text=True).lower()


def test_token_vencido_devuelve_401(app, client):
    registrar(client)
    vencido = create_access_token(identity='1', expires_delta=timedelta(seconds=-10))
    resp = client.post('/invite', json={'email': 'beto@test.com'}, headers=auth(vencido))
    assert resp.status_code == 401


def test_token_invalido_devuelve_401_sin_detalles(client):
    resp = client.post('/invite', json={'email': 'beto@test.com'}, headers=auth('esto-no-es-un-jwt'))
    assert resp.status_code == 401
    assert resp.get_json() == {'msg': 'Sesión inválida o vencida. Iniciá sesión de nuevo.'}


def test_token_de_un_usuario_que_ya_no_existe_devuelve_401(app, client):
    token = create_access_token(identity='999')
    resp = client.post('/invite', json={'email': 'beto@test.com'}, headers=auth(token))
    assert resp.status_code == 401


def test_el_correo_de_invitacion_incluye_el_enlace_de_registro(app, client):
    """CU0010: el correo lleva el enlace a la pantalla de registro (CU0006)."""
    registrar(client)
    token = token_de(client)
    with mail.record_messages() as enviados:
        client.post('/invite', json={'email': 'beto@test.com'}, headers=auth(token))
    assert 'http://localhost:4200/register' in enviados[0].body


def test_la_invitacion_enviada_queda_guardada_como_enviada(app, client):
    registrar(client)
    token = token_de(client)
    client.post('/invite', json={'email': 'Beto@Test.com'}, headers=auth(token))

    invitaciones = Invitation.query.all()
    assert len(invitaciones) == 1
    assert invitaciones[0].email == 'beto@test.com'
    assert invitaciones[0].status == Invitation.ENVIADA
    assert invitaciones[0].inviter.email == 'ana@test.com'
    assert invitaciones[0].created_at is not None


def test_si_falla_el_envio_la_invitacion_queda_guardada_como_fallida(app, client, monkeypatch):
    """CU0010 ca 5.1: el fallo queda registrado."""
    registrar(client)
    token = token_de(client)

    def smtp_caido(msg):
        raise ConnectionError('sin conexión')

    monkeypatch.setattr(mail, 'send', smtp_caido)
    client.post('/invite', json={'email': 'beto@test.com'}, headers=auth(token))

    assert [i.status for i in Invitation.query.all()] == [Invitation.FALLIDA]


def test_sin_sesion_o_con_correo_invalido_no_se_guarda_ninguna_invitacion(client):
    client.post('/invite', json={'email': 'beto@test.com'})
    registrar(client)
    token = token_de(client)
    client.post('/invite', json={'email': 'esto-no-es-un-correo'}, headers=auth(token))
    assert Invitation.query.count() == 0
