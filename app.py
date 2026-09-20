import sqlite3
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    message = session.pop("message", None)
    message_type = session.pop("message_type", None)
    return render_template("index.html", message=message, message_type=message_type)

@app.route("/new_recipe")
def new_recipe():
    return render_template("new_recipe.html")

@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    title = request.form["title"]
    description = request.form["description"]
    ingredients = request.form["ingredients"]
    instructions = request.form["instructions"]
    user_id = session["user_id"]
    sql = "INSERT INTO recipes (user_id, title, description, ingredients, instructions) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [user_id, title, description, ingredients, instructions])
    return redirect("/")

@app.route("/register")
def register():
    message = session.pop("message", None)
    message_type = session.pop("message_type", None)
    return render_template("register.html", message=message, message_type=message_type)

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        session["message"] = "Error: Passwords are not the same!"
        session["message_type"] = "error"
        return redirect("/register")
    
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        session["message"] = "Error: Username already taken!"
        session["message_type"] = "error"
        return redirect("/register")

    session["message"] = "Account created successfully!"
    session["message_type"] = "success"
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        message = session.pop("message", None)
        message_type = session.pop("message_type", None)
        return render_template("login.html", message=message, message_type=message_type)
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        res = db.query(sql, [username])
        
        if len(res) != 1:
            session["message"] = "Error: Incorrect username or password!"
            session["message_type"] = "error"
            return redirect("/login")

        user_id = res[0]["id"]
        password_hash = res[0]["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            session["message"] = "Error: Incorrect username or password!"
            session["message_type"] = "error"
            return redirect("/login")

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    return redirect("/")