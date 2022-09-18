from flask import Flask,render_template,request,session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    cards = db.relationship('Cards', backref ='author',lazy =True)

    def __repr__(self):
        return f"Users('{self.username}')"
class Cards(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable = False)
    concept = db.Column(db.String(50), nullable =False)
    explanation = db.Column(db.Text, nullable =False)
    photo = db.Column(db.String(20), nullable = False, default = 'default.jpg')

    def __repr__(self):
        return f"Cards('{self.concept}','{self.explanation}', '{self.photo}')"