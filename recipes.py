"""Helper functions for recipe-related database operations."""
import db

def get_all_categories():
    """Retrieves categories into dict. Used to display available category values."""
    sql = "SELECT category, value FROM categories ORDER BY id"
    res = db.query(sql)

    categories = {}
    for category, value in res:
        categories[category] = []
    for category, value in res:
        categories[category].append(value)

    return categories


def get_categories(recipe_id):
    """Helper function to retrieve and display categories for web pages."""
    sql = "SELECT category, value FROM recipe_categories WHERE recipe_id = ?"
    return db.query(sql, [recipe_id])


def add_recipe(user_id, form, categories):
    """Add a recipe and its categories to the database."""
    sql = """INSERT INTO recipes
             (user_id, title, description, ingredients, instructions)
             VALUES (?, ?, ?, ?, ?)"""

    db.execute(sql, [
        user_id,
        form["title"],
        form["description"],
        form["ingredients"],
        form["instructions"],
    ])

    recipe_id = db.last_insert_id()

    sql = """INSERT INTO recipe_categories (recipe_id, category, value)
             VALUES (?, ?, ?)"""

    for category, value in categories:
        db.execute(sql, [recipe_id, category, value])


def get_recipes():
    """Helper function for an empty search field."""
    sql = "SELECT id, user_id, title FROM recipes ORDER BY id DESC"
    return db.query(sql)


def get_recipe(recipe_id):
    """Helper function to display recipe contents for several pages."""
    sql = """SELECT users.username,
                    users.id AS user_id,
                    recipes.id,
                    recipes.title,
                    recipes.description,
                    recipes.ingredients,
                    recipes.instructions
             FROM recipes, users
             WHERE recipes.user_id = users.id AND 
                   recipes.id = ?"""
    res = db.query(sql, [recipe_id])
    return res[0] if res else None


def get_latest_recipe(user_id):
    """Fetches the newest recipe published by a user."""
    sql = """SELECT id, title, created_at
             FROM recipes
             WHERE user_id = ?
             ORDER BY id DESC
             LIMIT 1"""
    result = db.query(sql, [user_id])
    return result[0] if result else None


def get_recipes_with_images():
    """Retrieves associated fields with a given recipe, including owner and image.
       These are then displayed on index.html."""
    sql = """SELECT
                 r.*,
                 u.username AS author,
                 EXISTS (
                     SELECT 1
                     FROM images AS i
                     WHERE i.recipe_id = r.id
                 ) AS has_image,
                 COALESCE(rs.rating_count, 0) AS rating_count,
                 rs.avg_rating AS avg_rating
                 FROM recipes AS r
                 JOIN users AS u
                     ON u.id = r.user_id
                 LEFT JOIN (
                     SELECT
                         recipe_id,
                         AVG(rating) AS avg_rating,
                         COUNT(*) AS rating_count
                     FROM ratings
                     GROUP BY recipe_id
                 ) AS rs
                     ON rs.recipe_id = r.id
                 ORDER BY r.id DESC"""
    return db.query(sql)


def update_recipe(recipe_id, form):
    """Update an existing recipe and its categories."""
    sql = """UPDATE recipes
             SET title = ?,
                 description = ?,
                 ingredients = ?,
                 instructions = ?
             WHERE id = ?"""

    db.execute(sql, [
        form["title"],
        form["description"],
        form["ingredients"],
        form["instructions"],
        recipe_id
    ])

    sql = "DELETE FROM recipe_categories WHERE recipe_id = ?"
    db.execute(sql, [recipe_id])

    sql = """INSERT INTO recipe_categories
             (recipe_id, category, value)
             VALUES (?, ?, ?)"""

    for category, value in form["categories"]:
        db.execute(sql, [recipe_id, category, value])


def remove_recipe(recipe_id):
    """Handles removing a given recipe from the database."""
    sql = "DELETE FROM recipe_categories WHERE recipe_id = ?"
    db.execute(sql, [recipe_id])
    sql = "DELETE FROM recipes WHERE id = ?"
    db.execute(sql, [recipe_id])


def find_recipes(query):
    """Helper function for search recipe when given search string."""
    sql = """SELECT id, title
             FROM recipes
             WHERE title LIKE ? OR description LIKE ?
             ORDER BY id DESC"""
    return db.query(sql, ["%" + query + "%", "%" + query + "%"])


def find_recipes_by_categories(selected_categories, query=""):
    """Helper function to search all recipes associated with given categories."""
    conditions = []
    params = []

    for category, value in selected_categories:
        conditions.append(
            "(recipe_categories.category = ? AND recipe_categories.value = ?)"
        )
        params.extend([category, value])

    sql = """
        SELECT recipes.id, recipes.title
        FROM recipes
        JOIN recipe_categories
            ON recipes.id = recipe_categories.recipe_id
        WHERE (""" + " OR ".join(conditions) + ")"

    if query:
        sql += """
            AND (
                recipes.title LIKE ?
                OR recipes.description LIKE ?
            )"""

        params.extend(["%" + query + "%", "%" + query + "%"])

    sql += """
        GROUP BY recipes.id, recipes.title
        HAVING COUNT(
            DISTINCT recipe_categories.category || ':' || recipe_categories.value
        ) = ?
        ORDER BY recipes.id DESC"""
    params.append(len(selected_categories))
    return db.query(sql, params)


def get_rating(recipe_id):
    """Calculates avg. rating and total ratings for recipe, then rendered on show_recipe.html."""
    sql = """
        SELECT AVG(rating), COUNT(*)
        FROM ratings
        WHERE recipe_id = ?"""
    result = db.query(sql, (recipe_id,))[0]
    return result[0], result[1]


def get_ratings(recipe_id):
    """Fetches all newest ratings for given recipe and users who rated it."""
    sql = """SELECT ratings.id,
                    ratings.user_id,
                    ratings.rating,
                    users.username
             FROM ratings
             JOIN users ON ratings.user_id = users.id
             WHERE ratings.recipe_id = ?
             ORDER BY ratings.id DESC"""
    return db.query(sql, [recipe_id])


def get_user_rating(recipe_id, user_id):
    """Checks if user has rated recipe. Returns ratings id and score or None."""
    sql = """SELECT id, rating
             FROM ratings
             WHERE recipe_id = ? AND user_id = ?"""
    res = db.query(sql, [recipe_id, user_id])
    return res[0] if res else None


def get_rating_by_id(rating_id):
    """Rating lookup by id and returns associated recipe and user."""
    sql = """SELECT recipe_id, user_id
             FROM ratings
             WHERE id = ?"""
    res = db.query(sql, [rating_id])
    return res[0] if res else None


def add_rating(recipe_id, user_id, rating):
    """Adds a rating to a recipe by given user."""
    sql = """INSERT INTO ratings (recipe_id, user_id, rating)
             VALUES (?, ?, ?)"""
    db.execute(sql, [recipe_id, user_id, rating])


def update_rating(rating_id, user_id, rating):
    """Updates the rating for a recipe by given user."""
    sql = """UPDATE ratings
             SET rating = ?
             WHERE id = ? AND user_id = ?"""
    db.execute(sql, [rating, rating_id, user_id])


def remove_rating(rating_id, user_id):
    """Removes the ratings for a recipe by given user."""
    sql = """DELETE FROM ratings
             WHERE id = ? AND user_id = ?"""
    db.execute(sql, [rating_id, user_id])


def get_comments(recipe_id):
    """Retrieves all user comments for a given recipe."""
    sql = """SELECT comments.id,
                    comments.user_id,
                    comments.comment,
                    comments.created_at,
                    users.username
             FROM comments
             JOIN users ON comments.user_id = users.id
             WHERE comments.recipe_id = ?
             ORDER BY comments.id DESC"""
    return db.query(sql, [recipe_id])


def get_comment_by_id(comment_id):
    """Retrieves user comment for recipe by comment id."""
    sql = """SELECT id, recipe_id, user_id, comment
             FROM comments
             WHERE id = ?"""
    res = db.query(sql, [comment_id])
    return res[0] if res else None


def add_comment(recipe_id, user_id, comment):
    """ Adds a user comment to a recipe."""
    sql = """INSERT INTO comments (recipe_id, user_id, comment)
             VALUES (?, ?, ?)"""
    db.execute(sql, [recipe_id, user_id, comment])


def update_comment(comment_id, user_id, new_comment):
    """Updates a user comment for a recipe."""
    sql = """UPDATE comments
             SET comment = ?
             WHERE id = ? AND user_id = ?"""
    db.execute(sql, [new_comment, comment_id, user_id])


def remove_comment(comment_id, user_id):
    """Removes a user comment from a recipe."""
    sql = """DELETE FROM comments
             WHERE id = ? AND user_id = ?"""
    db.execute(sql, [comment_id, user_id])


def get_image(recipe_id):
    """Retrieves image file for associated recipe."""
    sql = "SELECT image FROM images WHERE recipe_id = ?"
    result = db.query(sql, [recipe_id])
    return result[0]["image"] if result else None


def update_image(recipe_id, image):
    """Updates an image to associated recipe."""
    sql = "UPDATE images SET image = ? WHERE recipe_id = ?"
    db.execute(sql, [image, recipe_id])


def save_image(recipe_id, image):
    """Saves or updates an image to associated recipe."""
    sql = """INSERT INTO images (recipe_id, image)
             VALUES (?, ?)
             ON CONFLICT(recipe_id)
             DO UPDATE SET image = excluded.image"""
    db.execute(sql, [recipe_id, image])


def remove_image(recipe_id):
    """"Removes associated image from a recipe."""
    sql = "DELETE FROM images WHERE recipe_id = ?"
    db.execute(sql, [recipe_id])
