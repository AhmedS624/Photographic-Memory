from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'e93064b6742da8b2dc4c66d6c61f55b5'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from final_project import routes