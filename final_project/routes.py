from datetime import datetime

from flask import render_template,request, session, flash, redirect,url_for,Response
from final_project import app,db,bcrypt
from final_project.forms import register_form,login_form,card_form
from final_project.Models import Users, Cards, Img
from flask_login import login_user, current_user,logout_user,login_required
from werkzeug.utils import secure_filename
from sqlalchemy.orm import load_only
from final_project.functions import getList



@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = login_form()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = Users.query.filter_by(email = form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect('/')
            else:
                flash('login Unsuccessful. Please check your email and password and try again','danger')
                return render_template('login.html', form = form)
    else:
                return render_template('login.html', form = form)



@app.route("/register", methods=["GET", "POST"])
def register():
    form = register_form()
    if current_user.is_authenticated:
        return redirect('/')
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username = form.username.data,email = form.email.data, password = hashed)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')
        return redirect('/login')
    else:
        
        return render_template('register.html', form = form)



@app.route("/")
@login_required
def home():
    return render_template("/home.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    logout_user()
    # Redirect user to login form
    return redirect("/login")


    
@app.route("/cards" ,methods = ('GET','POST'))
@login_required
def cards():
    form = card_form()
    if request.method == "GET":
        return render_template("/cards.html", form = form)
    else:
        if form.validate_on_submit:
            img = request.files['photo']
            if not img:
                return 'please uploade an img file',400
            filename = secure_filename(img.filename)
            mimetype = img.mimetype

            card = Cards(user_id = current_user.get_id(),concept = form.concept.data,explanation = form.explanation.data)

            db.session.add(card)
            db.session.commit()

            card_id = Cards.query.filter_by(concept = form.concept.data).first().id
            photo = Img(img=img.read(),mimetype = mimetype,name = filename, card_id = card_id,date = datetime.now())
            
            db.session.add(photo)
            db.session.commit()
            flash('Saved', 'success')
            return render_template("/cards.html", form = form)
        
@app.route("/browse-cards")
@login_required
def browse():
    user_id = current_user.get_id()
    li = db.session.execute(f'SELECT concept FROM cards WHERE cards.user_id = {user_id} ORDER BY cards.id').fetchall()
    concepts = getList(li)
    ex = db.session.execute(f'SELECT explanation FROM cards WHERE cards.user_id = {user_id} ORDER BY cards.id').fetchall()
    explanations = getList(ex)


    
    return render_template("/browse-cards.html",concepts = concepts,explanations = explanations)

@app.route("/<int:id>")
@login_required
def get_img(id):
    img = Img.query.filter_by(id = id).first()
    if not img:
        return 'nooooooo', 400
    return Response (img.img,mimetype = img.mimetype)

@app.route("/palaces")
@login_required
def palaces():
    return render_template("/Palaces.html")
