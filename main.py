from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from sqlalchemy import create_engine, text
from flask_mysqldb import MySQL
import MySQLdb.cursors
import mysql.connector
import re
import datetime
app = Flask(__name__)
app.secret_key = 'secret_key'




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

@app.route('/cart')
def cart():
    if 'cart' in session:
        cart_items = session['cart']
        total_price = calculate_total_price(cart_items)
        return render_template('cart.html', cart_items=cart_items, total_price=total_price)
    else:
        return render_template('cart.html', cart_items=[], total_price=0)

@app.route('/product_page', methods=['GET', 'POST'])
def product_page():
    products = conn.execute(text("SELECT * FROM Products")).fetchall()
    return render_template('product_page.html', products=products)


@app.route("/AddProducts", methods=["GET", "POST"])
def AddProducts():
    if request.method == "POST":
            result = conn.execute(text("select PID from Products Order By PID DESC;")).fetchone()
            latestID = result[0]
            print(latestID)
            newID = incrementID(latestID)
            title = request.form["title"]
            description = request.form["description"]
            warranty = int(request.form["warranty"])
            stock = int(request.form["stock"])
            price = float(request.form["price"])
            added_by_username = session["Username"]
            conn.execute(text("insert into Products () values (:newID, :title, :description, :warranty, :stock, :price, :added_by_username);"), {"newID": newID, "added_by_username" : added_by_username, "warranty" : warranty, "stock" : stock, "price" : price, "title" : title, "description" :description})
            conn.commit()
            conn.execute(text("Insert Into ProductHasDiscount (PID) values (:newID);"), {"newID": newID})
            conn.commit()
            colors = request.form.getlist("color")
            sizes = request.form.getlist("size")
            images = request.form.getlist("image")
            for color in colors:
                conn.execute(text("insert into ProductColor () values (:newID, :color);"), {"color":color, "newID":newID})
                conn.commit()
            for size in sizes:
                conn.execute(text("insert into ProductSize () values (:newID, :size);"), {"size":size, "newID":newID})
                conn.commit()
            for image in images:
                conn.execute(text("insert into ProductImages () values (:newID, :image);"), {"image":image, "newID":newID})
                conn.commit()  
    return render_template("AddProducts.html")

@app.route("/EditProducts", methods=["GET", "POST"])
def EditProduct():
    if request.method == "GET":
        result = conn.execute(text("""SELECT 
            P.PID,
            P.Title,
            P.Description,
            P.WarrantyPeriod,
            P.nOfItems,
            P.price,
            P.addedByUserName,
            (
                SELECT GROUP_CONCAT(D.DiscountAmount) 
                FROM ProductHasDiscount PHD 
                JOIN Discounts D ON PHD.DID = D.DID 
                WHERE PHD.PID = P.PID
            ) AS DiscountAmounts,
            (
                SELECT GROUP_CONCAT(D.timeTillActive) 
                FROM ProductHasDiscount PHD 
                JOIN Discounts D ON PHD.DID = D.DID 
                WHERE PHD.PID = P.PID
            ) AS TimeTillActive,
            (
                SELECT GROUP_CONCAT(PI.imageURL) 
                FROM ProductImages PI 
                WHERE PI.PID = P.PID
            ) AS ImageURLs,
            (
                SELECT GROUP_CONCAT(PC.color) 
                FROM ProductColor PC 
                WHERE PC.PID = P.PID
            ) AS Colors,
            (
                SELECT GROUP_CONCAT(PS.size) 
                FROM ProductSize PS 
                WHERE PS.PID = P.PID
            ) AS Sizes
        FROM Products P;""")).all()
        discounts = conn.execute(text("Select * from Discounts;")).all()
        formatted_discounts = [(d[0], d[1], d[2].strftime('%Y-%m-%d') if d[2] is not None else None) for d in discounts]
        print(discounts)
        print(formatted_discounts)
        print(result)
        return render_template("EditProducts.html", results=result, discounts=formatted_discounts)
    if request.method == "POST":
        print(request.form)
        edit_title = request.form.get("ProductAddedBy")
        print(edit_title)
        if edit_title == 'Edit Product Details':
            conn.execute(text("Update Products Set Title = :ProductName, Description = :ProductDescription, WarrantyPeriod = :ProductWarranty, nOfItems = :ProductStock, price = :ProductPrice, addedByUserName = :ProductAddedBy Where PID = :ProductID"), request.form)
            conn.commit()
        if edit_title == 'Edit Discount Details':
            conn.execute(text("Update ProductHasDiscount Set DID = :DiscountID Where PID = :ProductID;"), request.form)
            conn.commit()
    return render_template("EditProducts.html")

@app.route('/my_account')
def my_account():
    if 'loggedin' in session:
        username = session['Username']
        user = conn.execute(text("SELECT * FROM Users WHERE userName = :username"), {'username': username}).fetchone()
        return render_template('my_account.html', user=user)
    else:
        return redirect(url_for('login'))

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ilikegames05!",
    database="180Final"
)

# Function to fetch messages from the database
def fetch_messages(sender, recipient):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Messages WHERE (Sender = %s AND Recipient = %s) OR (Sender = %s AND Recipient = %s) ORDER BY ID", (sender, recipient, recipient, sender))
    messages = cursor.fetchall()
    return messages

# Function to save a new message to the database
def save_message(sender, recipient, content):
    cursor = db.cursor()
    cursor.execute("INSERT INTO Messages (Sender, Recipient, Content) VALUES (%s, %s, %s)", (sender, recipient, content))
    db.commit()

# Endpoint to send a message
@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    sender = data['sender']
    recipient = data['recipient']
    content = data['content']
    save_message(sender, recipient, content)
    return jsonify({"success": True})

# Endpoint to fetch messages
@app.route('/messages', methods=['GET'])
def get_messages():
    sender = request.args.get('sender')
    recipient = request.args.get('recipient')
    messages = fetch_messages(sender, recipient)
    return jsonify(messages)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template('chat.html')

@app.route('/my_orders')
def my_orders():
    # Fetch orders from the database
    with db.cursor() as cursor:
        sql = "SELECT * FROM Orders"
        cursor.execute(sql)
        orders = cursor.fetchall()

        # Fetch order items for each order
        for order in orders:
            sql = "SELECT Products.Title, Products.price FROM CartHasProduct JOIN Products ON CartHasProduct.PID = Products.PID WHERE CartHasProduct.cartID = %s"
            cursor.execute(sql, (order['OID'],))
            order['order_items'] = cursor.fetchall()

            # Calculate total price for each order
            total_price = sum(item['price'] for item in order['order_items'])
            order['total_price'] = total_price

    return render_template('my_orders.html', orders=orders)

@app.route('/review', methods=['GET'])
def review():
    # Get the product ID from the query parameters
    product_id = request.args.get('product_id')
    if product_id:
        # Render the review page, passing the product ID to the template
        return render_template('review.html', product_id=product_id)
    else:
        # Redirect to the product page if no product ID is provided
        return redirect(url_for('product_page'))

if __name__ == '__main__':
    app.run(debug=True)