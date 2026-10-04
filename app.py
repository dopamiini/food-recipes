import sqlite3
from flask import Flask, abort, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db, recipes, users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    message = session.pop("message", None)
    message_type = session.pop("message_type", None)
    all_recipes = recipes.get_recipes()
    return render_template("index.html", message=message, message_type=message_type, recipes=all_recipes)

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
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
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

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)

    if not user:
        abort(404)

    recipes = users.get_recipes(user_id)
    return render_template("show_user.html", user=user, recipes=recipes)

@app.route("/new_recipe")
def new_recipe():
    require_login()
    return render_template("new_recipe.html")

@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    require_login()

    title = request.form["title"]
    if len(title) > 50:
        abort(400)
    description = request.form["description"]
    if len(description) > 1000:
        abort(400)
    ingredients = request.form["ingredients"]
    if len(ingredients) > 10000:
        abort(400)
    instructions = request.form["instructions"]
    if len(instructions) > 1000:
        abort(400)
    user_id = session["user_id"]

    recipes.add_recipe(user_id, title, description, ingredients, instructions)

    return redirect("/")

@app.route("/find_recipe")
def find_recipe():
    query = request.args.get("query")
    if query:
        results = recipes.find_recipes(query)
    else:
        query = ""
        results = []
    return render_template("find_recipe.html", query=query, results=results)

@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    recipe = recipes.get_recipe(recipe_id)

    if not recipe:
        abort(404)
    
    return render_template("show_recipe.html", recipe=recipe)

@app.route("/edit_recipe/<int:recipe_id>")
def edit_recipe(recipe_id):
    require_login()

    recipe = recipes.get_recipe(recipe_id)

    if not recipe:
        abort(404)

    if recipe["user_id"] != session.get("user_id"):
        abort(403)

    return render_template("edit_recipe.html", recipe=recipe)

@app.route("/update_recipe", methods=["POST"])
def update_recipe():
    require_login()

    recipe_id = request.form["recipe_id"]
    title = request.form["title"]
    if len(title) > 50:
            abort(400)
    description = request.form["description"]
    if len(description) > 1000:
            abort(400)
    ingredients = request.form["ingredients"]
    if len(ingredients) > 1000:
            abort(400)
    instructions = request.form["instructions"]
    if len(instructions) > 1000:
            abort(400)

    recipe = recipes.get_recipe(recipe_id)
    
    if not recipe:
        abort(404)
    
    if recipe["user_id"] != session.get("user_id"):
        abort(403)
    
    recipes.update_recipe(recipe_id, title, description, ingredients, instructions)

    return redirect("/recipe/" + str(recipe_id))

@app.route("/remove_recipe/<int:recipe_id>", methods=["GET", "POST"])
def remove_recipe(recipe_id):
    require_login()
    
    recipe = recipes.get_recipe(recipe_id)

    if not recipe:
        abort(404)

    if recipe["user_id"] != session.get("user_id"):
        abort(403)

    if request.method == "GET":
        return render_template("remove_recipe.html", recipe=recipe)

    if request.method == "POST":
        if "remove" in request.form:
            recipes.remove_recipe(recipe_id)
            return redirect("/")
        else:
            return redirect("/recipe/" + str(recipe_id))