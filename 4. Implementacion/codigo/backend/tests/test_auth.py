"""CU0001 Iniciar Sesión y CU0006 Registrar Usuario, a través de la API."""

from conftest import login, registrar

from app.persistence.daos.user_dao import UserDAO


# --- CU0006 Registrar Usuario ---

def test_registro_exitoso_devuelve_201(client):
    resp = registrar(client)
    assert resp.status_code == 201
    assert resp.get_json()['email'] == 'ana@test.com'


def test_la_clave_se_guarda_con_hash_y_no_en_claro(app, client):
    registrar(client, password='password123')
    user = UserDAO.get_by_email('ana@test.com')
    assert user.password_hash != 'password123'
    assert 'password123' not in user.password_hash


def test_correo_ya_registrado_devuelve_409(client):
    registrar(client)
    resp = registrar(client)
    assert resp.status_code == 409
    assert resp.get_json()['msg'] == 'Este correo ya está registrado.'


def test_el_correo_no_distingue_mayusculas(client):
    registrar(client, email='ana@test.com')
    resp = registrar(client, email='ANA@Test.com')
    assert resp.status_code == 409


def test_clave_corta_devuelve_400_y_no_crea_el_usuario(app, client):
    resp = registrar(client, password='corta')
    assert resp.status_code == 400
    assert resp.get_json()['msg'] == 'Por favor complete todos los campos correctamente.'
    assert UserDAO.get_by_email('ana@test.com') is None


def test_registro_con_campos_faltantes_devuelve_400(client):
    resp = client.post('/auth/register', json={'email': 'ana@test.com'})
    assert resp.status_code == 400


# --- CU0001 Iniciar Sesión ---

def test_login_correcto_devuelve_token_y_datos_del_usuario(client):
    registrar(client)
    resp = login(client)
    assert resp.status_code == 200
    datos = resp.get_json()
    assert datos['access_token']
    assert datos['user'] == {'id': 1, 'name': 'Ana', 'email': 'ana@test.com'}


def test_login_con_clave_incorrecta_devuelve_401(client):
    registrar(client)
    resp = login(client, password='otra-clave')
    assert resp.status_code == 401
    assert 'access_token' not in resp.get_json()


def test_correo_inexistente_y_clave_incorrecta_dan_el_mismo_mensaje(client):
    """No se revela qué correos están registrados (CU0001, ca 5.1)."""
    registrar(client)
    clave_mal = login(client, password='otra-clave').get_json()
    no_existe = login(client, email='nadie@test.com').get_json()
    assert clave_mal == no_existe == {'msg': 'Credenciales incorrectas.'}


def test_login_con_campos_vacios_devuelve_400(client):
    resp = client.post('/auth/login', json={'email': '', 'password': ''})
    assert resp.status_code == 400
    assert resp.get_json()['msg'] == 'Por favor complete todos los campos correctamente.'
