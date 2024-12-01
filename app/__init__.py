from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.config import Config

app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt =Bcrypt(app)
migrate = Migrate(app, db)
admin = Admin(app, name="Event Arena", template_mode='bootstrap4')
login_manager = LoginManager(app)

from app.database import User, Role, Event, Visitor

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Event, db.session))
admin.add_view(ModelView(Visitor, db.session))
admin.add_view(ModelView(Role, db.session))


from app import routes
   

