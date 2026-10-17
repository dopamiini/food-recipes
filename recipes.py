import db

def get_all_categories():
    sql = "SELECT category, value FROM categories ORDER BY id"
    res = db.query(sql)

    categories = {}
    for category, value in res:
        categories[category] = []
    for category, value in res:
        categories[category].append(value)

    return categories

def add_recipe(user_id, title, description, ingredients, instructions, categories):
    sql = "INSERT INTO recipes (user_id, title, description, ingredients, instructions) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [user_id, title, description, ingredients, instructions])

    recipe_id = db.last_insert_id()

    sql = "INSERT INTO recipe_categories (recipe_id, category, value) VALUES (?, ?, ?)"
    for category, value in categories:
        db.execute(sql, [recipe_id, category, value])

def get_categories(recipe_id):
    sql = "SELECT category, value FROM recipe_categories WHERE recipe_id = ?"
    return db.query(sql, [recipe_id])

def get_recipes():
    sql = "SELECT id, user_id, title FROM recipes ORDER BY id DESC"
    return db.query(sql)

def get_recipe(recipe_id):
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

def update_recipe(recipe_id, title, description, ingredients, instructions, categories):
    sql = """UPDATE recipes
             SET title = ?,
                 description = ?,
                 ingredients = ?,
                 instructions = ?
             WHERE id = ?"""
    db.execute(sql, [title, description, ingredients, instructions, recipe_id])

    sql = "DELETE FROM recipe_categories WHERE recipe_id = ?"
    db.execute(sql, [recipe_id])

    sql = "INSERT INTO recipe_categories (recipe_id, category, value) VALUES (?, ?, ?)"
    for category, value in categories:
        db.execute(sql, [recipe_id, category, value])

def remove_recipe(recipe_id):
    sql = "DELETE FROM recipe_categories WHERE recipe_id = ?"
    db.execute(sql, [recipe_id])
    sql = "DELETE FROM recipes WHERE id = ?"
    db.execute(sql, [recipe_id])

def find_recipes(query):
    sql = """SELECT id, title
             FROM recipes
             WHERE title LIKE ? OR description LIKE ?
             ORDER BY id DESC"""
    return db.query(sql, ["%" + query + "%", "%" + query + "%"])

def get_rating(recipe_id):
    sql = """
        SELECT AVG(rating), COUNT(*)
        FROM ratings
        WHERE recipe_id = ?
    """

    result = db.query(sql, (recipe_id,))[0]
    return result[0], result[1]

def add_comment(recipe_id, user_id, comment):
    sql = """INSERT INTO comments (recipe_id, user_id, comment)
             VALUES (?, ?, ?)"""
    db.execute(sql, [recipe_id, user_id, comment])


def get_comments(recipe_id):
    sql = """SELECT comments.id, comments.user_id,
                    comments.comment, users.username
             FROM comments
             JOIN users ON comments.user_id = users.id
             WHERE comments.recipe_id = ?
             ORDER BY comments.id DESC"""
    return db.query(sql, [recipe_id])


def get_comment_by_id(comment_id):
    sql = """SELECT id, recipe_id, user_id, comment
             FROM comments
             WHERE id = ?"""
    res = db.query(sql, [comment_id])
    return res[0] if res else None


def remove_comment(comment_id, user_id):
    sql = """DELETE FROM comments
             WHERE id = ? AND user_id = ?"""
    db.execute(sql, [comment_id, user_id])


def get_ratings(recipe_id):
    sql = """SELECT ratings.id, ratings.user_id,
                    ratings.rating, users.username
             FROM ratings
             JOIN users ON ratings.user_id = users.id
             WHERE ratings.recipe_id = ?
             ORDER BY ratings.id DESC"""
    return db.query(sql, [recipe_id])


def get_user_rating(recipe_id, user_id):
    sql = """SELECT id, rating
             FROM ratings
             WHERE recipe_id = ? AND user_id = ?"""
    res = db.query(sql, [recipe_id, user_id])
    return res[0] if res else None


def add_rating(recipe_id, user_id, rating):
    sql = """INSERT INTO ratings (recipe_id, user_id, rating)
             VALUES (?, ?, ?)"""
    db.execute(sql, [recipe_id, user_id, rating])


def update_rating(rating_id, user_id, rating):
    sql = """UPDATE ratings
             SET rating = ?
             WHERE id = ? AND user_id = ?"""
    db.execute(sql, [rating, rating_id, user_id])


def remove_rating(rating_id, user_id):
    sql = """DELETE FROM ratings
             WHERE id = ? AND user_id = ?"""
    db.execute(sql, [rating_id, user_id])

    
def get_rating_by_id(rating_id):
    sql = """SELECT recipe_id, user_id
             FROM ratings
             WHERE id = ?"""
    res = db.query(sql, [rating_id])
    return res[0] if res else None