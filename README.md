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
# Get-Content .\schema.sql | sqlite3 .\database.d (Windows)
```

Run the app via `flask run`. Once the server is running, open `http://127.0.0.1:5000` in your browser to interact with the demo app.

## Testing the application

The app can be tested manually by following the checklists below or doing something similar. These should cover the current main functionalities of the application, including: registration, logging in, managing recipes, and searching.

1. Testing the registration functionality.
   * Open the registration page by clicking 'Register'.
   * Register a new user account and check the account is created successfully.
   * Try to register another account using the same username. This should fail and an error message is displayed.
   * Try using a different password in the password confirmation field and confirm this fails as above.

2. Testing logging in functionality.
   * Open the login page by clicking 'Sign in'.
   * Attempt login using a registered username and incorrect password. This should fail and an error message is displayed.
   * Attempt login with a random username that doesn't exist. Verify this fails and an error message is displayed.
   * Try login using a registered username and correct password. This should succeed and you are redirected to the main page.
   * Check if log out works and then login again.

3. Testing recipe functionality. Note that you need a registered account and must be logged in.
   * Try add a new recipe by clicking 'Add recipe'. Currently field values are not mandatory. After pressing 'Add' you should be redirected back to the main page.
   * Try to open the recipe from the recipe list. All relevant fields should be displayed.
   * Try to edit your own recipe by clicking 'Edit'. This should display the previous field values and allow you to edit them. Change some value and click 'Update'. This should redirect you back to the recipes page and update the values.
   * Try to remove your own recipe by clicking 'Remove'. This should remove it and redirect you to the main page.
   * Now logout and open a recipe from the list. Check that the edit and remove functionalities are not available to other users.

4. You can test the search function by searching for a recipe by name without being logged in. An empty field should show all  recipes.

## Basic functional requirements:

* In the app the user can register an account and then login using that account.
* The user can add, edit and remove their own recipes. The recipes include the required ingredients and cooking instructions.
* The user can view all recipes listed on the app.
* The user can search for recipes using keywords and optionally filter recipes by category.
* The app has a user page that shows information about the user and their added recipes.
  * It shows the number of recipes the user has added.
  * It shows a list of all the recipes the user has added.
* The user can assign one or more categories to a recipe. Categories are divided into the following types:
  * **Recipe type:** appetizer, main course, or dessert
  * **Diet:** lactose-free, gluten-free, or vegan
* The user can comment and rate other recipes.
  * Recipes will show user comments.
  * Recipes will show the average rating score.

## Additional functionalities:

* Unregistered users can still view recipes but are not able to add, modify, comment, or rate recipes.
* The user can add a picture to their recipe.
* The user can sort recipes by date using options such as **"Newest"**.

## Data Entities

The primary entity is a **recipe**, and the secondary entity is a **comment** associated with a recipe.

## Comments

Note that the requirements may be updated during the project, but none of the mandatory basic requirements will be removed. Current working idea for the app name is Recepio. A rough first sketch of the app can be found [here](images/food-recipes.png).
