
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_admin import Admin


db = SQLAlchemy()
bcrypt =Bcrypt()
migrate = Migrate()
admin = Admin(name="Event Arena", template_mode='bootstrap4')
login_manager = LoginManager()