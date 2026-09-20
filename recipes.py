import db

def add_recipe(user_id, title, description, ingredients, instructions):
    sql = "INSERT INTO recipes (user_id, title, description, ingredients, instructions) VALUES (?, ?, ?, ?, ?)"
    db.execute(sql, [user_id, title, description, ingredients, instructions])

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

    if len(res) != 1:
        return None

    return res[0]

def update_recipe(recipe_id, title, description, ingredients, instructions):
    sql = """UPDATE recipes
             SET title = ?,
                 description = ?,
                 ingredients = ?,
                 instructions = ?
             WHERE id = ?"""

    db.execute(sql, [
        title,
        description,
        ingredients,
        instructions,
        recipe_id
    ])

def delete_recipe(recipe_id):
    sql = "DELETE FROM recipes WHERE id = ?"
    db.execute(sql, [recipe_id])

def search_recipes(search):
    sql = """SELECT id, user_id, title
             FROM recipes
             WHERE title LIKE ?
             ORDER BY id DESC"""

    return db.query(sql, ["%" + search + "%"])