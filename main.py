from flask import Flask, render_template, request, redirect, url_for, session, flash
from sqlalchemy import create_engine, text
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'secret_key'



# connection string is in the format mysql://user:password@server/database
conn_str = "mysql://root:Ilikegames05!@localhost/180final"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()


def noCustAlow():
    typeU = session["UserType"]
    if typeU == "Customer":
        return False
    elif typeU == "Admin" or typeU == "Vendor":
        return True


def CheckexistUser(username):
     username = str(username)
     account = conn.execute(text("SELECT username FROM Users WHERE username = :username;"), {'username': username})
     result = account.fetchone()
     if result:
         return True
     else:
        return False

def CheckexistEmail(email):
     email = str(email)
     account = conn.execute(text("SELECT username FROM Users WHERE email = :email;"), {'email': email})
     result = account.fetchone()
     if result:
         return True
     else:
        return False
     
def incrementID(ID):
    ID = str(ID)
    fletter = ID[0]
    number = int(ID[1:])
    next = number + 1
    final = f'{fletter}{next}'
    return final



@app.route("/")
def index():
    if 'loggedin' in session:
        return render_template("index.html")
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        account = conn.execute(text("SELECT * FROM Users WHERE username = :username"), request.form)
        user_data = account.fetchone()
        flash(f"{user_data}", "error")
        print(user_data)
        if user_data is None:
            flash("Account does not exist", 'error')
            return render_template('login.html', username=username)
        elif user_data[3] != password:
            flash("Incorrect Password", 'error')
            return render_template('login.html', username=username)
        elif user_data:
            session['loggedin'] = True
            session['Username'] = user_data[0]
            session["Name"] = user_data[1]
            session["UserType"] = user_data[4]
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('Username', None)
    session.pop('Name', None)
    session.pop('UserType', None)
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        accountType = request.form['accountType']
        if CheckexistUser(username):
            flash('This Username Already Exists!', 'error')
            return render_template('signup.html', email=email, name=name)
        elif CheckexistEmail(email):
            flash('This Email Already Exists!', 'error')
            return render_template('signup.html', username=username, name=name)
        else:
            conn.execute(text("insert into users () values (:username, :name, :email, :password, :accountType)"), {"username": username, "name": name, "email": email, "password": password, "accountType": accountType}).all()
            conn.commit()
            session['loggedin'] = True
            session['Username'] = username
            session["Name"] = name
            session["UserType"] = accountType
            return redirect(url_for("index"))
    return render_template('signup.html')

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    return render_template('cart.html')

@app.route('/productpage', methods=['GET', 'POST'])
def productpage():
    return render_template('product_page.html')


@app.route("/AddProducts", methods=["GET", "POST"])
def AddProducts():
    if request.method == "POST":
        result = conn.execute(text("select PID from Products Order By PID DESC;")).fetchone()
        latestID = result[0]
        print(latestID)
        newID = incrementID(latestID)
        # title = request.form["title"]
        # description = request.form["description"]
        # warranty = int(request.form["warranty_period"])
        # stock = int(request.form["n_of_items"])
        # price = float(request.form["price"])
        # added_by_username = session["Username"]

        
        colors = request.form.getlist("color")
        sizes = request.form.getlist("size")
        images = request.form.getlist("image")
    return render_template("AddProducts.html")

if __name__ == '__main__':
    app.run(debug=True)