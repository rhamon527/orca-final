import pytest
from app import app, db, User, Department, Obra

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()
        # Adiciona dados de teste
        dept = Department(name='RH')
        obra = Obra(name='TesteObra')
        db.session.add(dept)
        db.session.add(obra)
        db.session.commit()

        user = User(name='Admin', email='admin@example.com',
                    department=dept, obra=obra)
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()

    yield client

def test_login(client):
    response = client.post('/login', data={
        'email': 'admin@example.com',
        'password': '123456'
    }, follow_redirects=True)
    assert b'Seja bem-vindo' in response.data
