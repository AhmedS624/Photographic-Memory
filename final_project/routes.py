from datetime import datetime
import secrets
import os


from flask import render_template,request, session, flash, redirect,url_for,Response
from final_project import app,db,bcrypt
from final_project.forms import register_form,login_form,card_form,selectPalace_form
from final_project.Models import Users, Cards,Routes,Palaces
from flask_login import login_user, current_user,logout_user,login_required
from werkzeug.utils import secure_filename
from sqlalchemy.orm import load_only
from final_project.functions import getList,getDict



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

# functions that needs to be here

def card_route(li):
    routes=[]
    for i in range(len(li)):
        foo = getList(db.session.execute(f'SELECT route FROM routes WHERE id = "{li[i]}" ').fetchall())
        routes.append(foo[0])
    return routes



def save_img(form_img):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_img.filename)
    img_fn = random_hex + f_ext
    img_path = os.path.join(app.root_path,'static/photos',img_fn)
    form_img.save(img_path)
    return img_fn


def getRoute(li,ri):

    rm_route = []
    new_list = list(set(ri).difference(li))
    for i in range(len( new_list )):
        one_check = getList(db.session.execute(f'SELECT route FROM routes WHERE id = {new_list[i]}').fetchall())
        rm_route.append(one_check[0])
    return rm_route


    
@app.route("/select_palace" ,methods = ('GET','POST'))
@login_required
def select_palace():
    form = selectPalace_form()
    palaces_names = getList(db.session.execute(f'SELECT name FROM palaces ').fetchall())
    if request.method == 'GET':
        for i in range(len(palaces_names)):
            form.name.choices.append((palaces_names[i],palaces_names[i]))
        return render_template('select_palace.html',palaces_names = palaces_names,form = form)

    else:
        if form.validate_on_submit:
            name = form.name.data
            session['palace_selected'] = name
            return redirect('/cards')



@app.route("/browse-palaces")
@login_required
def browse_palaces():
    user_id = current_user.get_id()
    try:
        palaces = getList(db.session.execute(f'SELECT name FROM palaces ').fetchall())
       
    except:
        return "you don't have any palaces create some then comeback"
    
  
    tup = (db.session.execute('select name,route from routes join palaces on palace_id = palaces.id').fetchall())
    dic = {}

    eve = getDict(tup, dic)

    # card section

    card_id = getList(db.session.execute(f'SELECT id FROM cards WHERE cards.user_id = {user_id} ORDER BY cards.id').fetchall())[0]

    li = db.session.execute(f'SELECT concept FROM cards WHERE cards.user_id = {user_id} ORDER BY cards.id').fetchall()
    concepts = getList(li)
    ex = db.session.execute(f'SELECT explanation FROM cards WHERE cards.user_id = {user_id} ORDER BY cards.id').fetchall()
    explanations = getList(ex)
    img_name = getList(db.session.execute(f'SELECT img FROM cards ORDER BY cards.id').fetchall())

    route_id = getList(db.session.execute('select route_id from cards').fetchall())

    x= 0


    return render_template("/browse-palaces.html",palaces = palaces,eve = eve ,
                            concepts = concepts,explanations = explanations,img_name = img_name,route_id = route_id)

@app.route("/palace",methods = ['GET','POST'])
@login_required
def create_palace():
    if request.method == 'GET':
        return render_template("/palace.html")
    else:
        palace = request.form.get('palace')
        palace_list = getList(db.session.execute(f'SELECT name FROM palaces ').fetchall())
        if palace in palace_list:
            flash('You already have this palace','danger')
            return redirect('/palace')
        else:

            palac = Palaces(name = palace)
            session['palace_name'] = palace

            db.session.add(palac)
            db.session.commit()
            return redirect('/route')

@app.route("/route",methods = ['GET','POST'])
@login_required
def route():
    palace_name = session.get('palace_name',None)
    palace_id = getList(db.session.execute(f'SELECT id FROM palaces WHERE palaces.name = "{palace_name}";').fetchall())[0]
    roads = getList(db.session.execute(f'SELECT route FROM Routes WHERE palace_id = {palace_id};'))

    if request.method == 'GET':
        try:
            return render_template("/routes.html" ,roads = roads)
        except:
            return render_template("/routes.html")

    else:     
            check_point = request.form.get('check_point')

            route_list = getList(db.session.execute(f'SELECT route FROM routes ').fetchall())
            if check_point in route_list:
                flash('You already have this route','danger')
                return redirect('/route')
            else:

                route = Routes(route = check_point,palace_id = palace_id)

                db.session.add(route)
                db.session.commit()

                roads = getList(db.session.execute(f'SELECT route FROM Routes WHERE palace_id = {palace_id};'))
                return render_template("/routes.html" ,roads = roads)








@app.route("/cards" ,methods = ('GET','POST'))
@login_required
def cards():
    form = card_form()
    palace_name = session.get('palace_selected',None)
    palace_id = getList(db.session.execute(f'SELECT id FROM palaces WHERE palaces.name = "{palace_name}"').fetchall())[0]
    routes_ids = getList(db.session.execute(f'SELECT id FROM routes WHERE palace_id = "{palace_id}"'))

    # when you select a route it disappears from the select menu
    trash = getList(db.session.execute(f'SELECT id FROM routes WHERE palace_id = "{palace_id}" INTERSECT SELECT route_id FROM cards ').fetchall())

    routes = getRoute(trash,routes_ids)
    

    for i in range(len(routes)):
            form.route.choices.append((routes[i],routes[i]))

    if request.method == "GET":
        return render_template("/cards.html", form = form,routes = routes)
    else:
        if form.validate_on_submit:
            img_file = save_img(form.photo.data)
            ch_route = form.route.data

            route_id = getList(db.session.execute(f'SELECT id FROM routes WHERE route = "{ch_route}"').fetchall())[0]


            #add to the form which palace and on that which route to add : done
            #add routes to the cards : done
            card = Cards(user_id = current_user.get_id(),concept = form.concept.data,explanation = form.explanation.data,img=img_file,route_id = route_id)

            db.session.add(card)
            db.session.commit()
            
            flash('Saved', 'success')
            return redirect("/cards")
        
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
    img_name = getList(db.session.execute(f'SELECT img FROM cards ORDER BY cards.id').fetchall())

    route_id = getList(db.session.execute(f'SELECT route_id FROM cards ').fetchall())
    routes = card_route(route_id)

    
    return render_template("/browse-cards.html",concepts = concepts,explanations = explanations,img_name = img_name,routes = routes)

