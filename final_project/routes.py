from datetime import datetime
import secrets
import os


from flask import render_template,request, session, flash, redirect,url_for,Response
from final_project import app,db,bcrypt
from final_project.forms import register_form,login_form,card_form
from final_project.Models import Users, Cards
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

def save_img(form_img):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_img.filename)
    img_fn = random_hex + f_ext
    img_path = os.path.join(app.root_path,'static/photos',img_fn)
    form_img.save(img_path)
    return img_fn

    
@app.route("/cards" ,methods = ('GET','POST'))
@login_required
def cards():
    form = card_form()
    if request.method == "GET":
        return render_template("/cards.html", form = form)
    else:
        if form.validate_on_submit:
            img_file = save_img(form.photo.data)

            card = Cards(user_id = current_user.get_id(),concept = form.concept.data,explanation = form.explanation.data,img=img_file)

            db.session.add(card)
            db.session.commit()
            
            flash('Saved', 'success')
            return render_template("/cards.html", form = form)
        
@app.route("/browse-cards")
@login_required
def browse():
    user_id = current_user.get_id()
    try:
        card_id = getList(db.session.execute(f'SELECT id FROM cards WHERE cards.user_id = {user_id} ORDER BY cards.id').fetchall())[0]
    except:
        return "you don't have any cards create some then comeback"
    li = db.session.execute(f'SELECT concept FROM cards WHERE cards.user_id = {user_id} ORDER BY cards.id').fetchall()
    concepts = getList(li)
    ex = db.session.execute(f'SELECT explanation FROM cards WHERE cards.user_id = {user_id} ORDER BY cards.id').fetchall()
    explanations = getList(ex)
    img_name = getList(db.session.execute(f'SELECT img FROM cards ORDER BY cards.id').fetchall()
)



    
    return render_template("/browse-cards.html",concepts = concepts,explanations = explanations,img_name = img_name)


@app.route("/palaces")
@login_required
def palaces():
    return render_template("/Palaces.html")
