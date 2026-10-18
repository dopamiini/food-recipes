import sqlite3
from flask import Flask, abort, redirect, render_template, request, session
from datetime import datetime
import config
import db, recipes, secrets, users

app = Flask(__name__)
app.secret_key = config.secret_key


MAX_IMAGE_SIZE = 5 * 1024 * 1024


def require_login():
    if "user_id" not in session:
        abort(403)


def check_csrf():
    if request.form.get("csrf_token") != session.get("csrf_token"):
        abort(403)


def get_flash_messages():
    message = session.pop("message", None)
    message_type = session.pop("message_type", None)

    return message, message_type


def is_valid_png(data):
    if not data or len(data) > MAX_IMAGE_SIZE:
        return False

    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return False

    return True


def validate_recipe_form():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    ingredients = request.form.get("ingredients", "").strip()
    instructions = request.form.get("instructions", "").strip()

    all_categories = recipes.get_all_categories()
    selected_categories = request.form.getlist("categories")

    message = None

    if not title:
        message = "Recipe title is required."
    elif len(title) > 50:
        message = "Recipe title must be at most 50 characters."
    elif not description:
        message = "Recipe description is required."
    elif len(description) > 80:
        message = "Recipe description must be at most 80 characters."
    elif not ingredients:
        message = "Ingredients are required."
    elif len(ingredients) > 500:
        message = "Ingredients must be at most 500 characters."
    elif not instructions:
        message = "Recipe instructions are required."
    elif len(instructions) > 500:
        message = "Instructions must be at most 500 characters."

    categories = []

    for entry in selected_categories:
        if not entry:
            continue

        parts = entry.split(":", 1)

        if len(parts) != 2:
            abort(400)

        category, value = parts

        if category not in all_categories:
            abort(403)

        if value not in all_categories[category]:
            abort(403)

        categories.append((category, value))

    if not message:
        for group in all_categories:
            if not any(category == group for category, value in categories):
                message = "Please select an option for " + group + "."
                break

    return {
        "title": title,
        "description": description,
        "ingredients": ingredients,
        "instructions": instructions,
        "all_categories": all_categories,
        "selected_categories": selected_categories,
        "categories": categories,
        "message": message,
    }


@app.template_filter("eu_datetime")
def eu_datetime(value):
    dt = datetime.strptime(value, "%Y-%m-%d %H:%M")
    return dt.strftime("%d.%m.%Y %H:%M")


@app.route("/")
def index():
    message, message_type = get_flash_messages()

    all_recipes = recipes.get_recipes_with_images()
    
    return render_template(
        "index.html",
        message=message,
        message_type=message_type,
        recipes=all_recipes,
    )


@app.route("/find_recipe")
def find_recipe():
    query = request.args.get("query", "").strip()

    if len(query) > 80:
        abort(400)

    categories = recipes.get_all_categories()

    selected_values = list(dict.fromkeys(request.args.getlist("category")))

    selected_categories = []

    for entry in selected_values:
        parts = entry.split(":", 1)

        if len(parts) != 2:
            abort(400)

        category, value = parts

        if category not in categories or value not in categories[category]:
            abort(400)

        selected_categories.append((category, value))

    if selected_categories:
        results = recipes.find_recipes_by_categories(selected_categories, query)
    elif query:
        results = recipes.find_recipes(query)
    else:
        results = recipes.get_recipes()

    return render_template(
        "find_recipe.html",
        query=query,
        results=results,
        result_count=len(results),
        categories=categories,
        selected_categories=selected_values,
    )


@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    recipe = recipes.get_recipe(recipe_id)

    if not recipe:
        abort(404)

    message, message_type = get_flash_messages()

    categories = recipes.get_categories(recipe_id)
    comments = recipes.get_comments(recipe_id)

    ratings = recipes.get_ratings(recipe_id)
    average_rating, rating_count = recipes.get_rating(recipe_id)

    user_rating = None
    if session.get("user_id"):
        user_rating = recipes.get_user_rating(
            recipe_id, session["user_id"]
        )

    has_image = recipes.get_image(recipe_id) is not None

    return render_template(
        "show_recipe.html",
        recipe=recipe,
        categories=categories,
        comments=comments,
        ratings=ratings,
        average_rating=average_rating,
        rating_count=rating_count,
        user_rating=user_rating,
        message=message,
        message_type=message_type,
        has_image=has_image,
    )


@app.route("/recipe/<int:recipe_id>/comments")
def show_recipe_comments(recipe_id):
    recipe = recipes.get_recipe(recipe_id)

    if not recipe:
        abort(404)

    comments = recipes.get_comments(recipe_id)

    return render_template(
        "show_comments.html",
        recipe=recipe,
        comments=comments,
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        message, message_type = get_flash_messages()
        username = session.pop("login_username", "")

        return render_template(
            "login.html",
            message=message,
            message_type=message_type,
            username=username,
        )
    else:
        username = request.form["username"].strip()
        password = request.form["password"]

        if not username or not password:
            session["message"] = "Username and password are required."
            session["message_type"] = "error"
            session["login_username"] = username
            return redirect("/login")

        user = users.check_login(username, password)

        if user:
            session.pop("login_username", None)
            session["user_id"] = user["id"]
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")

        session["message"] = "Incorrect username or password!"
        session["message_type"] = "error"
        session["login_username"] = username
        return redirect("/login")


@app.route("/logout", methods=["POST"])
def logout():
    require_login()
    check_csrf()

    session.pop("user_id", None)
    session.pop("username", None)

    return redirect("/")


@app.route("/register")
def register():
    message, message_type = get_flash_messages()
    username = session.pop("register_username", "")

    return render_template(
        "register.html", 
        message=message,
        message_type=message_type,
        username=username,
    )


@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"].strip()
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if not username:
        message = "Username is required."
        session.pop("register_username", None)
    
    elif users.get_user_username(username):
        message = "Username already exists!"

    elif not password1:
        message = "Password is required!"

    elif not password2:
        message = "Please confirm your password!"

    elif password1 != password2:
        message = "Passwords are not the same!"

    else:
        message = None

    if message:
        session["message"] = message
        session["message_type"] = "error"

        if username:
            session["register_username"] = username

        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        session["message"] = "Username is already taken!"
        session["message_type"] = "error"
        return redirect("/register")

    session["message"] = "Account has been created successfully!"
    session["message_type"] = "success"
    return redirect("/")


@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user_id(user_id)

    if not user:
        abort(404)

    latest_recipe = recipes.get_latest_recipe(user_id)
    user_recipes = users.get_recipes(user_id)

    #recipes = users.get_recipes(user_id)
    return render_template(
        "show_user.html",
        user=user,
        recipes=user_recipes,
        latest_recipe=latest_recipe,
    )


@app.route("/new_recipe")
def new_recipe():
    require_login()

    categories = recipes.get_all_categories()

    message, message_type = get_flash_messages()

    return render_template(
        "new_recipe.html",
        message=message,
        message_type=message_type,
        title="",
        description="",
        ingredients="",
        instructions="",
        categories=categories,
        selected_categories=[],
    )


@app.route("/create_recipe", methods=["POST"])
def create_recipe():
    require_login()
    check_csrf()

    form = validate_recipe_form()

    if form["message"]:
        return render_template(
            "new_recipe.html",
            message=form["message"],
            message_type="error",
            title=form["title"],
            description=form["description"],
            ingredients=form["ingredients"],
            instructions=form["instructions"],
            categories=form["all_categories"],
            selected_categories=form["selected_categories"],
        )

    user_id = session["user_id"]

    recipes.add_recipe(
        user_id,
        form["title"],
        form["description"],
        form["ingredients"],
        form["instructions"],
        form["categories"],
    )

    session.pop("recipe_form", None)
    session["message"] = "Recipe created successfully!"
    session["message_type"] = "success"

    return redirect("/")


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

    return render_template(
        "edit_recipe.html",
        recipe=recipe,
        categories=categories,
        all_categories=all_categories,
    )


@app.route("/update_recipe", methods=["POST"])
def update_recipe():
    require_login()
    check_csrf()

    recipe_id = request.form.get("recipe_id", type=int)

    if recipe_id is None:
        abort(400)

    recipe = recipes.get_recipe(recipe_id)

    if not recipe:
        abort(404)

    if recipe["user_id"] != session.get("user_id"):
        abort(403)

    form = validate_recipe_form()

    categories = {
        group: ""
        for group in form["all_categories"]
    }

    for category, value in form["categories"]:
        categories[category] = value

    if form["message"]:
        recipe_data = dict(recipe)

        recipe_data["title"] = form["title"]
        recipe_data["description"] = form["description"]
        recipe_data["ingredients"] = form["ingredients"]
        recipe_data["instructions"] = form["instructions"]

        return render_template(
            "edit_recipe.html",
            recipe=recipe_data,
            categories=categories,
            all_categories=form["all_categories"],
            message=form["message"],
            message_type="error",
        )

    recipes.update_recipe(
        recipe_id,
        form["title"],
        form["description"],
        form["ingredients"],
        form["instructions"],
        form["categories"],
    )

    session["message"] = "Recipe updated successfully!"
    session["message_type"] = "success"

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
        return render_template(
            "remove_recipe.html",
            recipe=recipe,
        )

    if request.method == "POST":
        check_csrf()

        if "remove" in request.form:
            recipes.remove_recipe(recipe_id)
            return redirect("/")
        else:
            return redirect("/recipe/" + str(recipe_id))


@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()
    check_csrf()

    recipe_id = request.form.get("recipe_id", type=int)

    if recipe_id is None:
        abort(400)

    recipe = recipes.get_recipe(recipe_id)

    if not recipe:
        abort(404)

    user_id = session["user_id"]
    comment = request.form.get("comment", "").strip()

    if not comment:
        session["message"] = "Comments cannot be empty."
        session["message_type"] = "error"
        return redirect("/recipe/" + recipe_id)

    if len(comment) > 200:
        session["message"] = "Comments must be at most 200 characters."
        session["message_type"] = "error"
        return redirect("/recipe/" + str(recipe_id))

    recipes.add_comment(recipe_id, user_id, comment)

    return redirect("/recipe/" + str(recipe_id))


@app.route("/edit_comment/<int:comment_id>", methods=["GET", "POST"])
def edit_comment(comment_id):
    require_login()

    comment = recipes.get_comment_by_id(comment_id)

    if not comment:
        abort(404)

    if comment["user_id"] != session.get("user_id"):
        abort(403)

    if request.method == "GET":
        return render_template(
            "edit_comment.html",
            comment=comment,
        )

    if request.method == "POST":
        check_csrf()

        new_comment = request.form.get("comment", "").strip()

        if not new_comment:
            session["message"] = "Comment cannot be empty."
            session["message_type"] = "error"
            return render_template(
                "edit_comment.html",
                comment=comment,
                comment_text=new_comment,
            )

        recipes.update_comment(
            comment["id"],
            session["user_id"],
            new_comment,
        )

        session["message"] = "Comment updated successfully!"
        session["message_type"] = "success"

        return redirect("/recipe/" + str(comment["recipe_id"]))


@app.route("/remove_comment/<int:comment_id>", methods=["GET", "POST"])
def remove_comment(comment_id):
    require_login()

    comment = recipes.get_comment_by_id(comment_id)

    if not comment:
        abort(404)

    if comment["user_id"] != session.get("user_id"):
        abort(403)

    if request.method == "GET":
        return render_template(
            "remove_comment.html",
            comment=comment,
        )

    if request.method == "POST":
        check_csrf()

        if "remove" in request.form:
            recipes.remove_comment(comment_id, session["user_id"])
            print("Redirecting to:", "/recipe/" + str(comment["recipe_id"]))
            return redirect("/recipe/" + str(comment["recipe_id"]))
        else:
            print("Redirecting to:", "/recipe/" + str(comment["recipe_id"]))
            return redirect("/recipe/" + str(comment["recipe_id"]))


@app.route("/create_rating", methods=["POST"])
def create_rating():
    require_login()
    check_csrf()

    recipe_id = request.form.get("recipe_id", type=int)
    rating = request.form.get("rating", type=int)

    if recipe_id is None:
        abort(400)

    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)

    if rating is None:
        session["message"] = "Rating is required."
        session["message_type"] = "error"
        return redirect("/recipe/" + str(recipe_id))
    
    if not 1 <= rating <= 5:
        abort(400)

    user_id = session["user_id"]

    existing_rating = recipes.get_user_rating(recipe_id, user_id)
    if existing_rating:
        abort(409, description="You have already rated this recipe.")

    recipes.add_rating(recipe_id, user_id, rating)

    return redirect("/recipe/" + str(recipe_id))


@app.route("/edit_rating", methods=["POST"])
def edit_rating():
    require_login()
    check_csrf()

    rating_id = request.form.get("rating_id", type=int)
    rating = request.form.get("rating", type=int)

    if rating_id is None:
        abort(400)

    existing_rating = recipes.get_rating_by_id(rating_id)

    if not existing_rating:
            abort(404)

    user_id = session["user_id"]

    if existing_rating[1] != user_id:
        abort(403)

    recipe_id = existing_rating[0]

    if rating is None:
        session["message"] = "Rating is required."
        session["message_type"] = "error"
        return redirect("/recipe/" + str(recipe_id))

    if not 1 <= rating <= 5:
        abort(400)

    recipes.update_rating(rating_id, user_id, rating)

    return redirect("/recipe/" + str(recipe_id))


@app.route("/remove_rating", methods=["POST"])
def remove_rating():
    require_login()
    check_csrf()

    rating_id = request.form.get("rating_id", type=int)

    if rating_id is None:
        abort(400)

    user_id = session["user_id"]

    existing_rating = recipes.get_rating_by_id(rating_id)

    if not existing_rating:
        abort(404)

    if existing_rating[1] != user_id:
        abort(403)

    recipe_id = existing_rating[0]

    recipes.remove_rating(rating_id, user_id)

    return redirect("/recipe/" + str(recipe_id))


@app.route("/upload_image/<int:recipe_id>", methods=["POST"])
def upload_image(recipe_id):
    require_login()
    check_csrf()

    recipe = recipes.get_recipe(recipe_id)
    if not recipe:
        abort(404)

    if recipe["user_id"] != session["user_id"]:
        abort(403)

    uploaded_file = request.files.get("image")

    if uploaded_file is None or not uploaded_file.filename:
        session["message"] = "Please select a PNG image."
        session["message_type"] = "error"
        return redirect("/recipe/" + str(recipe_id))

    image_data = uploaded_file.stream.read(MAX_IMAGE_SIZE + 1)

    if not is_valid_png(image_data):
        session["message"] = "Invalid PNG image or image exceeds 5 MB."
        session["message_type"] = "error"
        return redirect("/recipe/" + str(recipe_id))

    recipes.save_image(recipe_id, image_data)

    session["message"] = "Image uploaded successfully!"
    session["message_type"] = "success"

    return redirect("/recipe/" + str(recipe_id))


@app.route("/remove_image/<int:recipe_id>", methods=["GET", "POST"])
def remove_image(recipe_id):
    require_login()

    recipe = recipes.get_recipe(recipe_id)

    if not recipe:
        abort(404)

    if recipe["user_id"] != session.get("user_id"):
        abort(403)

    if request.method == "POST":
        check_csrf()

        if request.form.get("action") == "Remove":
            recipes.remove_image(recipe_id)

            session["message"] = "Recipe image removed successfully!"
            session["message_type"] = "success"

        return redirect("/recipe/" + str(recipe_id))

    return render_template("remove_image.html", recipe=recipe)


@app.route("/recipe_image/<int:recipe_id>")
def recipe_image(recipe_id):
    image = recipes.get_image(recipe_id)

    if image is None:
        abort(404)

    return image, 200, {"Content-Type": "image/png"}