# Import Libraries
import os
import json
import datetime
import random
from flask import Flask, render_template, request, redirect, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_mail import Mail, Message
from tempfile import mkdtemp
from werkzeug.exceptions import MethodNotAllowed, default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helper import login_required, apology

# Configure application
app = Flask(__name__)

# Configure mail fucntionality
mail = Mail(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Start application in debug mode
app.config["DEBUG"] = True

# Tracks modifications in database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# Database integration
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://deepank:deepank@localhost/samplestore"
db = SQLAlchemy(app)

# configuration of mail
app.config['MAIL_SERVER']='smtpout.secureserver.net'
app.config['MAIL_PORT'] = 80
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# WepApp endpoints

# Index Page
@app.route("/")
def index():
    
    # User reached route via GET
    filename = os.path.join(app.static_folder, "store.json")
    with open(filename) as store:
        store = json.load(store)

    for item in store:
        item_name = str(item["item_name"])
        item_price = str(item["item_price"])
        item_image = str(item["item_image"])
        new_arrival = str(item["new_arrival"])

    return render_template("index.html", new_arrivals=store)


# View Store 
@app.route("/store", methods=["GET", "POST"])
def store():

    # User reached route via GET
    if request.method == "GET":
        filename = os.path.join(app.static_folder, "store.json")
        with open(filename) as store:
            store = json.load(store)

        for item in store:
            item_name = str(item["item_name"])
            item_price = str(item["item_price"])
            item_image = str(item["item_image"])

            isItemPresent = db.engine.execute("SELECT item_name FROM store WHERE item_name = %s;", item_name)

            if isItemPresent.rowcount != 1:
                db.engine.execute("INSERT INTO store (item_name, item_price, item_image) VALUES (%s, %s, %s);", item_name, item_price, item_image)
            
            store_items = db.engine.execute("SELECT * FROM store;")

        return render_template("store.html", store_items=store_items)

# About Page
@app.route("/about")
def about():

    # Render a static about page
    return render_template("about.html")

# Login Functionality
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        if not username:
            return apology("must provide username", 400)

        elif not password:
            return apology("must provide password", 400)

        # Query database for username
        rows = db.engine.execute("SELECT * FROM users WHERE username = %s", username).fetchone()
       
        # Ensure username exists and password is correct
        try:
            if len(rows) == None or not check_password_hash(rows[2], password):
                return apology("invalid username and/or password", 400)
        except Exception:
            return apology("user does not exist", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]
        session["username"] = rows[1]

        # Redirect user to home page
        return redirect("/store")

    # User reached out via GET
    else:
        return render_template("login.html")

# Registering a user
@app.route("/register", methods=["GET", "POST"])
def register():

    # Variables taken from the register form
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    # User reached route via GET
    if request.method == "GET":
        return render_template("register.html")

    # User reached route via POST
    else:

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 400)
        
        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("Must provide password", 400)
        
        # Ensure password was repeated
        if not request.form.get("confirmation"):
            return apology("Must repeat password", 400)
        
        # Matching password
        if password != confirmation:
            return apology("password didn't match", 400)    

        # Hashing the password
        password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        # Adding user to the database
        try:
            db.engine.execute("INSERT INTO users (username, password) VALUES (%s, %s);", username, password_hash)
        
        # If the user already exists
        except Exception:
            return apology("username already exist!", 400)

        # Success message
        flash("User Registered")

        # Prompt user to login after registering
        return render_template("login.html")

# Log out a user
@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# Add to cart
@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():

    # Ensure cart exists
    if "cart" not in session:
        session["cart"] = []
    
    # Route for POST
    if request.method == "POST":
        item_id = request.form.get("id")
        if item_id:
            session["cart"].append(item_id)
        return redirect("/cart")
    
    # Adding item to the cart
    items = list()
    total = 0
    for i in session["cart"]:
        items.append(db.engine.execute("SELECT * FROM store WHERE item_id = %s", i).fetchone())
        total += int(db.engine.execute("SELECT item_price FROM store WHERE item_id = %s ", i).fetchone()[0])

    return render_template("cart.html", items=items, total=total)

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    if request.method == "GET":
        user_id = session["user_id"]
        profile = db.engine.execute("SELECT * FROM users WHERE id = %s", user_id).fetchone()
        # print(profile)
        return render_template("profile.html", profile=profile)

    else:

        # Taking variables from the form
        user_id = request.form.get("user_id")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        address = request.form.get("address")

        print(user_id)
        if username:
            try:
                db.engine.execute("UPDATE users set username = %s where id = %s;", username, user_id)
                session["username"] = username
                flash("username updated!")
        
            except Exception:
                return apology("username couldn't be updated. Please try again!", 400)    
        
        if not password and confirmation:
            return apology("Must enter password twice", 400)
        if password:

            if not confirmation:
                return apology("Must repeat password", 400)

            # Matching passwords
            if password != confirmation:
                return apology("password didn't match", 400)

            # Hashing the password
            password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
            
            # Updating password
            try:
                db.engine.execute("UPDATE users set password = %s where id = %s;", password_hash, user_id)
                flash("password updated!")
        
            except Exception:
                return apology("password couldn't be updated. Please try again!", 400)

        if address:
            # Updating address
            try:
                db.engine.execute("UPDATE users set address = %s where id = %s;", address, user_id)
                flash("address updated!")
        
            except Exception:
                return apology("address couldn't be updated. Please try again!", 400)
  
        return redirect("/profile")


# Checkout        
@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    
    total = int(request.form.get("total"))
    
    items = list()
    for i in session["cart"]:
        items.append(db.engine.execute("SELECT * FROM store WHERE item_id = %s", i).fetchone())
    
    freeShipping = False
    shippingCharges = 5
    if total > 0:
        if total > 20:
            freeShipping = True
            shippingCharges = 0
        
        grandTotal = total + shippingCharges

        address = db.engine.execute("SELECT address FROM users WHERE id = %s;", session["user_id"]).fetchone()
        print(address)
        return render_template("checkout.html", total=total, items=items, freeShipping=freeShipping, shippingCharges=shippingCharges, grandTotal=grandTotal, address=address)
    else:
        return apology("Your cart is empty! Please add something to your cart", 400)


# Order Success
@app.route("/success", methods=["GET", "POST"])
@login_required
def success():
    
    # Fetch the items in the cart
    items = list()
    for i in session["cart"]:
        items.append(db.engine.execute("SELECT * FROM store WHERE item_id = %s", i).fetchone())
    
    # Get the order timestamp
    timeOfOrder = datetime.datetime.now()

    # Random external order id generation
    ext_id = str(timeOfOrder.date()) + "/" + str(random.randrange(10000, 99999))

    # Get the grand total from the form
    order_value = request.form.get("grandTotal")

    # Fetch the email id to send confirmation mail
    email = request.form.get("email")

    # GET Route
    if request.method == "GET":

        # Fetch order detail from the database
        order_details = db.engine.execute("SELECT * FROM orders WHERE ext_id = %s", session["ext_id"]).fetchone()
        print(session["ext_id"])
        print(order_details)
        # Empty the cart
        session["cart"] = []

        return render_template("success.html", items=items, order_details=order_details)

    # POST route
    else:
        
        # Order items to be saved in database
        order_items = list()
        for item in items:
            order_items.append(item["item_name"])

        order_items = json.dumps(order_items)

        # Store the external order id in session
        session["ext_id"] = ext_id
        
        # Inserting into the database
        db.engine.execute("INSERT INTO orders (ext_id, order_value, order_items, date, user_id) VALUES (%s, %s, %s, %s, %s);", session["ext_id"], order_value, order_items, timeOfOrder, session["user_id"])

        # Sending email
        msg = Message(
        'Order Confirmed',
        sender = os.getenv('MAIL_USERNAME'),
        recipients = [email]
        )
        msg.body = "Your order has been confirmed!\n\nYour order id is: " + ext_id + "\nEstimated delivery time will be 6-10 business days.\n\n" + "\nThanks for shopping with us.\nSampleStore Team"
        mail.send(msg)
        flash("Confirmation email sent")
        
        return redirect("/success")


# My Orders
@app.route("/myorders", methods=["GET"])
@login_required
def myorders():
    
    # Fetching all the user orders
    orderList = db.engine.execute("SELECT * FROM orders WHERE user_id = %s;", str(session["user_id"]))
    
    return render_template("myorders.html", orderList=orderList)


# Handle error
def errorhandler(e):
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
