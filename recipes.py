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


def find_recipes_by_categories(selected_categories, query=""):
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


def update_comment(comment_id, user_id, new_comment):
    sql = """
        UPDATE comments
        SET comment = ?
        WHERE id = ? AND user_id = ?
    """
    db.execute(sql, [new_comment, comment_id, user_id])


def get_comments(recipe_id):
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


def add_image(recipe_id, image):
    sql = "INSERT INTO images (recipe_id, image) VALUES (?, ?)"
    db.execute(sql, [recipe_id, image])


def get_image(recipe_id):
    sql = "SELECT image FROM images WHERE recipe_id = ?"
    result = db.query(sql, [recipe_id])
    return result[0]["image"] if result else None


def update_image(recipe_id, image):
    sql = "UPDATE images SET image = ? WHERE recipe_id = ?"
    db.execute(sql, [image, recipe_id])


def save_image(recipe_id, image):
    sql = """INSERT INTO images (recipe_id, image)
             VALUES (?, ?)
             ON CONFLICT(recipe_id)
             DO UPDATE SET image = excluded.image"""
    db.execute(sql, [recipe_id, image])


def remove_image(recipe_id):
    sql = "DELETE FROM images WHERE recipe_id = ?"
    db.execute(sql, [recipe_id])


def get_recipes_with_images():
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