from app.database import User, Role, Visitor, Event
from app.extentions import db
from datetime import datetime, timedelta
from app import app
import secrets
import pytest



def test_role_model():
    role = Role(name="Admin", description="Administrator role")
    assert role.name == "Admin"
    assert role.description == "Administrator role"

    
def test_user_model(client):  
    user = User(username="testuser", email="test@example.com", password="securepassword", user_role_id=1, fs_uniquifier=secrets.token_urlsafe(14))
    db.session.add(user)
    db.session.commit()


def test_user_model_err(client):
    with pytest.raises(ValueError) as info:
        user = User(username="testuser", email="test@example.com", password="securepassword", user_role_id=1, fs_uniquifier=secrets.token_urlsafe(14))
        db.session.add(user)
        db.session.commit()
        assert info


def test_event_model():
    future_date = datetime.now() + timedelta(days=1)  
    event = Event(name="Future Event", date=future_date, description="A future event")
    assert event.name == "Future Event"


def test_visitor_model(client):
    visitor = Visitor(user_email="test@example.com", phone="1234567890", event_id=1)
    assert visitor.user_email == "test@example.com"
