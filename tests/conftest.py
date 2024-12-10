from app import  app
from app.extentions import db
import pytest
import os
from flask_login import FlaskLoginClient
from app.utils import check_empty_role


@pytest.fixture()
def my_app():
    flask_app = app
    flask_app.config.update({
        "TESTING":True
    })
    yield app


@pytest.fixture(scope="module")
def client():
    os.environ['CONFIG_TYPE'] = "config.TestingConfig"
    flask_app = app
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client
            db.drop_all()


@pytest.fixture()
def form_client():
    print('\n login in user')


# @pytest.fixture(scope='module')
# def app_context():    
#     with app.app_context():
#         db.create_all()
#         yield app
#         db.session.remove()
#         db.drop_all()


