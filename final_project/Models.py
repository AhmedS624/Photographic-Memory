from final_project import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(120),unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    
    cards = db.relationship('Cards', backref ='author',lazy =True)

    def __repr__(self):
        return f"Users('{self.username}','{self.email}')"
class Cards(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'), nullable = False)
    concept = db.Column(db.String(50), nullable =False)
    explanation = db.Column(db.Text, nullable =False)
    img = db.Column(db.String(20), nullable =False,unique = True)
    route_id = db.Column(db.Integer,db.ForeignKey('routes.id'),nullable = False )

    def __repr__(self):
        return f"Cards('{self.concept}','{self.explanation}',{self.img})"
class Routes(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    palace_id = db.Column(db.Integer,db.ForeignKey('palaces.id'), nullable = False)
    route = db.Column(db.String(50), nullable = False,unique = True)
   
    cards = db.relationship('Cards', backref ='route',lazy =True)

    def __repr__(self):
        return f"Users('{self.route}','{self.palace_id}')"

class Palaces(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(50), unique = True, nullable = False)
   
    routes = db.relationship('Routes', backref ='palace',lazy =True)

    def __repr__(self):
        return f"Users('{self.id}','{self.name}')"

