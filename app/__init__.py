from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_jwt_extended import JWTManager
from flask_admin.contrib.sqla import ModelView



app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SUPER_SECRET')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event.db'
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False

db = SQLAlchemy(app)
bcrypt =Bcrypt(app)
migrate = Migrate(app, db)
admin = Admin(app, name="Event Arena", template_mode='bootstrap4')
jwt = JWTManager(app)

from app.database import User, Role, Event, Visitor

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Event, db.session))
admin.add_view(ModelView(Visitor, db.session))
admin.add_view(ModelView(Role, db.session))

from app import routes


   

