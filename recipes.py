import db

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

def update_recipe(recipe_id, title, description, ingredients, instructions):
    sql = """UPDATE recipes
             SET title = ?,
                 description = ?,
                 ingredients = ?,
                 instructions = ?
             WHERE id = ?"""
    db.execute(sql, [title, description, ingredients, instructions, recipe_id])

def remove_recipe(recipe_id):
    sql = "DELETE FROM recipes WHERE id = ?"
    db.execute(sql, [recipe_id])

def find_recipes(query):
    sql = """SELECT id, title
             FROM recipes
             WHERE title LIKE ? OR description LIKE ?
             ORDER BY id DESC"""
    return db.query(sql, ["%" + query + "%", "%" + query + "%"])