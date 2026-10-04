# Food Recipes (Recepio)

The app currently allows registered users to create, edit, and remove their own recipes. All users can view and search all recipes. The user can register an account and login using it. Navigating and using the app should be intuitive.

## Requirements

Git and Python 3.10 or newer.

## Installation and Setup

```bash
git clone https://github.com/dopamiini/food-recipes
cd food-recipes

# Initialize the database as follows:
# sqlite3 database.db < schema.sql (Linux)
# Get-Content .\schema.sql | sqlite3 .\database.db (Windows)
```

Run the app via `flask run`. Once the server is running, open `http://127.0.0.1:5000` in your browser to interact with the demo app.

## Recent updates ✓

All the current requirements for the milestone and previous milestones should be met.

* Added user access and authorization checks for protected pages and actions (add, edit, delete).
* Added input validation before storing data in the database.
* Added user profile pages with statistics and the user's recipes.
* Added two database-backed categories to recipes.
* Added comments so logged in users can provide comments on other users' recipes.

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
  * Recipes will show the average rating score. ❌

## Additional functionalities:

* Unregistered users can still view recipes but are not able to add, modify, comment, or rate recipes. ✅
* The user can add a picture to their recipe. ❌
* The user can sort recipes by date using options such as **"Newest"**. ❌

## Data Entities

The primary entity is a **recipe**, and the secondary entity is a **comment** associated with a recipe.

## Comments

Note that the requirements may be updated during the project, but none of the mandatory basic requirements will be removed. Current working idea for the app name is Recepio. A rough first sketch of the app can be found [here](images/food-recipes.png).

## Testing

Testing documentation and test cases can be found [here](documents/testing.md).
