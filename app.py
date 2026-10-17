import sqlite3
from flask import Flask, abort, redirect, render_template, request, session
import config
import db, recipes, secrets, users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if request.form.get("csrf_token") != session.get("csrf_token"):
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
    else:
        username = request.form["username"]
        password = request.form["password"]

        user = users.check_login(username, password)

        if user:
            session["user_id"] = user["id"]
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")

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

    try:
        users.create_user(username, password1)
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
    categories = recipes.get_all_categories()
    return render_template("new_recipe.html", categories=categories)

@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    require_login()
    check_csrf()

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

    all_categories = recipes.get_all_categories()

    categories= []
    for entry in request.form.getlist("categories"):
        if entry:
            parts = entry.split(":")
            if parts[0] not in all_categories:
                abort(403)
            if parts[1] not in all_categories[parts[0]]:
                abort(403)
            categories.append((parts[0], parts[1]))
    
    recipes.add_recipe(user_id, title, description, ingredients, instructions, categories)

    return redirect("/")

@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()
    check_csrf()

    recipe_id = request.form["recipe_id"]
    user_id = session["user_id"]
    comment = request.form["comment"]

    recipes.add_comment(recipe_id, user_id, comment)

    return redirect("/recipe/" + recipe_id)


@app.route("/create_rating", methods=["POST"])
def create_rating():
    if not session.get("user_id"):
        abort(403)

    recipe_id = request.form.get("recipe_id", type=int)
    rating = request.form.get("rating", type=int)

    if recipe_id is None or rating is None:
        abort(400)

    if not 1 <= rating <= 5:
        abort(400)

    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)

    user_id = session["user_id"]

    # A user may only rate a recipe once.
    existing_rating = recipes.get_user_rating(recipe_id, user_id)
    if existing_rating:
        abort(409, description="You have already rated this recipe.")

    recipes.add_rating(recipe_id, user_id, rating)

    return redirect("/recipe/" + str(recipe_id))


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

    categories = recipes.get_categories(recipe_id)
    comments = recipes.get_comments(recipe_id)

    ratings = recipes.get_ratings(recipe_id)
    average_rating, rating_count = recipes.get_rating(recipe_id)

    user_rating = None
    if session.get("user_id"):
        user_rating = recipes.get_user_rating(
            recipe_id, session["user_id"]
        )

    return render_template(
        "show_recipe.html",
        recipe=recipe,
        categories=categories,
        comments=comments,
        ratings=ratings,
        average_rating=average_rating,
        rating_count=rating_count,
        user_rating=user_rating
    )


@app.route("/edit_recipe/<int:recipe_id>")
def edit_recipe(recipe_id):
    require_login()

    recipe = recipes.get_recipe(recipe_id)

    if not recipe:
        abort(404)

    if recipe["user_id"] != session.get("user_id"):
        abort(403)

    all_categories = recipes.get_all_categories()
    categories = {}
    for group in all_categories:
        categories[group] = ""
    for entry in recipes.get_categories(recipe_id):
        categories[entry["category"]] = entry ["value"]

    return render_template("edit_recipe.html", recipe=recipe, categories=categories, all_categories=all_categories)

@app.route("/update_recipe", methods=["POST"])
def update_recipe():
    require_login()
    check_csrf()

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

    all_categories = recipes.get_all_categories()

    categories= []
    for entry in request.form.getlist("categories"):
        if entry:
            parts = entry.split(":")
            if parts[0] not in all_categories:
                abort(403)
            if parts[1] not in all_categories[parts[0]]:
                abort(403)
            categories.append((parts[0], parts[1]))

    recipes.update_recipe(recipe_id, title, description, ingredients, instructions, categories)

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
        check_csrf()
        
        if "remove" in request.form:
            recipes.remove_recipe(recipe_id)
            return redirect("/")
        else:
            return redirect("/recipe/" + str(recipe_id))


@app.route("/edit_rating", methods=["POST"])
def edit_rating():
    if not session.get("user_id"):
        abort(403)

    rating_id = request.form.get("rating_id", type=int)
    rating = request.form.get("rating", type=int)

    if rating_id is None or rating is None:
        abort(400)

    if not 1 <= rating <= 5:
        abort(400)

    user_id = session["user_id"]

    # Find the rating before editing it
    existing_rating = recipes.get_rating_by_id(rating_id)

    if not existing_rating:
        abort(404)

    # Only the owner can edit the rating
    if existing_rating[1] != user_id:
        abort(403)

    recipe_id = existing_rating[0]

    recipes.update_rating(rating_id, user_id, rating)

    return redirect("/recipe/" + str(recipe_id))


@app.route("/remove_rating", methods=["POST"])
def remove_rating():
    if not session.get("user_id"):
        abort(403)

    rating_id = request.form.get("rating_id", type=int)

    if rating_id is None:
        abort(400)

    user_id = session["user_id"]

    # Find the rating before removing it
    existing_rating = recipes.get_rating_by_id(rating_id)

    if not existing_rating:
        abort(404)

    # Only the owner can remove the rating
    if existing_rating[1] != user_id:
        abort(403)

    recipe_id = existing_rating[0]

    recipes.remove_rating(rating_id, user_id)

    return redirect("/recipe/" + str(recipe_id))


@app.route("/remove_comment/<int:comment_id>", methods=["GET", "POST"])
def remove_comment(comment_id):
    require_login()

    comment = recipes.get_comment_by_id(comment_id)

    if not comment:
        abort(404)

    if comment["user_id"] != session.get("user_id"):
        abort(403)

    if request.method == "GET":
        return render_template("remove_comment.html", comment=comment)

    if request.method == "POST":
        check_csrf()

        if "remove" in request.form:
            recipes.remove_comment(comment_id, session["user_id"])
            print("Redirecting to:", "/recipe/" + str(comment["recipe_id"]))
            return redirect("/recipe/" + str(comment["recipe_id"]))
        else:
            print("Redirecting to:", "/recipe/" + str(comment["recipe_id"]))
            return redirect("/recipe/" + str(comment["recipe_id"]))