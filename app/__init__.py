from flask import Flask
from app.extentions import admin, db, migrate, bcrypt, login_manager
from app.config import Config
from flask_admin.contrib.sqla import ModelView



app = Flask(__name__)
app.config.from_object(Config)
bcrypt.init_app(app)
db.init_app(app)
migrate.init_app(app, db)
admin.init_app(app)
login_manager.init_app(app)
from app.database import User, Role, Event, Visitor
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Event, db.session))
admin.add_view(ModelView(Visitor, db.session))
admin.add_view(ModelView(Role, db.session))

with app.app_context():
    from app import routes
    db.create_all()
   

    

    
    

