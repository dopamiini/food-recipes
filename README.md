# Food Recipes (Recepio)

The app currently allows registered users to create, edit, and remove their own recipes. All users can view and search all recipes. The user can register an account and login using it. Navigating and using the app should be intuitive.

## Running the Application

You need Python version 3.10 or later.

### 1. Clone the repository and navigate to the project directory

```bash
git clone https://github.com/dopamiini/food-recipes
cd food-recipes
```

### 2. Create a virtual environment and install Flask

**Linux and macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell):**

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Initialize the database

This command creates the database using the `schema.sql` file.

**Linux and macOS:**

```bash
python3 init_db.py
```

**Windows:** Use `python` instead of `python3`.

```powershell
python init_db.py
```

### 4. Start the application

```bash
flask run
```

The application will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Basic functional requirements:

* In the app the user can register an account and then login using that account. ✅
* The user can add, edit and remove their own recipes. The recipes include the required ingredients and cooking instructions. ✅
* The user can view all recipes listed on the app. ✅
* The user can search for recipes using keywords and optionally filter recipes by category. ✅
* The app has a user page that shows information about the user and their added recipes.
  * It shows the number of recipes the user has added. ✅
  * It shows a list of all the recipes the user has added. ✅
* The user can assign one or more categories to a recipe. Categories are divided into the following types: 
  * **Recipe type:** appetizer, main course, or dessert ✅
  * **Diet:** lactose-free, gluten-free, or vegan ✅
* The user can comment and rate other recipes.
  * Recipes will show user comments. ✅
  * Recipes will show the average rating score. ✅

## Additional functionalities:

* Unregistered users can still view recipes but are not able to add, modify, comment, or rate recipes. ✅
* The user can add a picture to their recipe. ✅

## Data Entities

The primary entity is a **recipe**, and the secondary entity is a **comment** associated with a recipe.

## Comments

Note that the requirements may be updated during the project, but none of the mandatory basic requirements will be removed. Current working idea for the app name is Recepio. A rough first sketch of the app can be found [here](images/food-recipes.png).

## Testing

## Pylint

Pylint report is in the file pylint-report.md

Testing documentation and test cases can be found [here](documents/testing.md).
