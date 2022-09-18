from flask import Flask,render_template,request,session
from forms import register_form,login
from Models import Users,Cards,db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e93064b6742da8b2dc4c66d6c61f55b5'

@app.route("/login", methods=["GET", "POST"])
def login():
    form = login()
    return render_template('login.html', form = form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = register_form()
    return render_template('register.html', form = form)



@app.route("/")
#@login_required
def home():
    return render_template("/home.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


    
@app.route("/cards" ,methods = ('GET','POST'))
#@login_required
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
#@login_required
def palaces():
    return render_template("/Palaces.html")

if __name__ == '__main__':
    app.run(debug=True)