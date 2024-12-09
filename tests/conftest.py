from app import  app
from app.extentions import db
import pytest
import os
from flask_login import FlaskLoginClient


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

@pytest.fixture()
def setUp_model():
    os.environ['CONFIG_TYPE'] = "config.TestingConfig"
    print("\nSetting Up Method......")
    flask_app = app
    with flask_app.test_client() as client:
        with flask_app.app_context():
            db.create_all()

    def clear_all_data():
        print("\nTearing down Method....")
        db.session.remove()
        db.drop_all()
        return client
    
    # request.addfinalizer(clear_all_data)
 


# @pytest.fixture(scope='module')
# def app_context():    
#     with app.app_context():
#         db.create_all()
#         yield app
#         db.session.remove()
#         db.drop_all()


