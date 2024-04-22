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



def Checkexist(username):
     username = str(username)
     account = conn.execute(text("SELECT username FROM Users WHERE username = :username"), {'username': username})
     result = account.fetchone()
     if result:
         return True
     else:
        return False

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
        account = conn.execute(text("SELECT * FROM Users WHERE username = :username AND password = :password"), request.form)
        user_data = account.fetchone()
        if not user_data:
            flash("Account does not exist", 'error')
            return redirect(url_for('login'))
        elif user_data:
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ''

if __name__ == '__main__':
    app.run(debug=True)