import pytest
from app.models.crystal import Crystal
from app import create_app
from app import db
from flask.signals import request_finished


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_saved_crystals(app):
    # Arrange
    amethyst_crystal = Crystal(name="amethyst",color="purple",powers="rest and relaxation")
    quartz_crystal = Crystal(name="quartz",color="white",powers="loveeeee")

    db.session.add_all([amethyst_crystal, quartz_crystal])

    # could alternatively do:
    # db.session.add(amethyst_crystal)
    # db.session.add(quartz_crystal)

    db.session.commit()