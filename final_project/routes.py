from flask import render_template,request, session, flash, redirect
from final_project import app,db,bcrypt
from final_project.forms import register_form,login_form
from final_project.Models import Users, Cards
from flask_login import login_user, current_user,logout_user,login_required



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
    if current_user.is_authenticated:
        return redirect('/')
    form = register_form()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username = form.username.data,email = form.email.data, password = hashed)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')
        return redirect('/login')
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
    if request.method == "GET":
        return render_template("/cards.html")
    else:
        concept = request.form.get("concept")
        img = request.files["img"]
        explanation = request.form.get("explanation")
        if not concept or img or explanation:
            return 'somthing is missing',400

        

@app.route("/palaces")
@login_required
def palaces():
    return render_template("/Palaces.html")
