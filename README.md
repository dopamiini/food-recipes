# Food Recipes (Recepio)

Recepio is a web application that allows users to publish their food recipes. All users can browse and search all recipes. Only registered users can create recipes and manage them. Registered users can also rate any recipe once and add comments to any recipes. All recipes have ingredients and instructions listed, as well as meal type and dietary information listed. There is also the option to add a photo of your dish to your recipe. Navigating and using the app should be intuitive.

## Running the Application

You need Python version 3.10 and Flask version 3.1.x or later.

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

This command creates the database using the `schema.sql` and `init.sql` files.

**Linux and macOS:**

```bash
python3 seed.py
```

Windows users use `python` instead of `python3`. You can always reset the database by rerunning the command.

### 4. Start the application

```bash
flask run
```

The application will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Functionality:

* All users can view all recipes listed on the app.
* All users can search for recipes using keywords and optionally filter recipes by category.
* Users can register an account and then login using that account.
* Registered user can add, edit and remove their own recipes. All recipe fields are mandatory, and adding pictures are optional.
* The app has a user page that shows information about the user and their added recipes.
  * It shows the number of recipes the user has added.
  * It lists all the recipes the user has added.
* The user can assign one or more categories to a recipe. Categories are divided into the following types: 
  * **Type:** Breakfast, Lunch, Dinner, Snack, Dessert
  * **Diet:** None, Keto, Dairy-free, Paleo, Vegan
* Registered users can comment and rate other recipes.
  * Recipes show user comments. Each user can make multiple comments on each recipe.
  * Recipes show the average rating score. Each user can only rate a single recipe once.

## Data Entities

The primary entity is a **recipe**, and the secondary entity is a **comment** associated with a recipe.

## Comments

Note that the requirements may be updated during the project, but none of the mandatory basic requirements will be removed. Current working idea for the app name is Recepio. A rough first sketch of the app can be found [here](images/food-recipes.png).

## Testing

Testing documentation and test cases can be found in the file [testing.md](documents/testing.md).

## Pylint

Pylint report is in the file [pylint-report.md](documents/pylint-report.md)
