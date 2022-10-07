from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rmbzggmgwckisa:d3cb08acf1ff822d2b30efde57b540309d811c738bede3847cb8defcff9ac15c@ec2-3-214-2-141.compute-1.amazonaws.com:5432/d76kf0sbgv38ql'

app.config['SECRET_KEY'] = 'e93064b6742da8b2dc4c66d6c61f55b5'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from final_project import routes