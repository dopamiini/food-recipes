CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE recipe_categories (
    id INTEGER PRIMARY KEY,
    recipe_id INTEGER REFERENCES recipes,
    category TEXT,
    value TEXT
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    category TEXT,
    value
);