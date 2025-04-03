from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path


db = SQLAlchemy()
DB_NAME = 'database.db'
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] =  'bjorn-fagel-horn'
    app.config['SQLALCHEMY_DATABASE_URI'] = F'sqlite:///{DB_NAME}'
        
    from .views import views
    from .auth import auth
    from .models import UserAccount, TaskList

    
    db.init_app(app)
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view= 'auth.login'
    login_manager.init_app(app)

    
    @login_manager.user_loader
    def load_user(id):
        return UserAccount.query.get(int(id))

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app

def create_database(e):
    if not path.exists(DB_NAME):
        with e.app_context():
            db.create_all() 