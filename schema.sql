CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS recipe_categories (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER,
    category TEXT,
    value TEXT,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    category TEXT,
    value TEXT
);

CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    comment TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ratings (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER UNIQUE NOT NULL,
    user_id INTEGER UNIQUE NOT NULL,
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS images (
    recipe_id INTEGER PRIMARY KEY,
    image BLOB NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);