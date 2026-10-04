## Testing the application

The app can be tested manually by following the checklists below or doing something similar. These should cover the current main functionalities of the application, including: registration, logging in, managing recipes, and searching.

1. Testing the registration functionality.
   * Open the registration page by clicking 'Register'. ✅
   * Register a new user account and check the account is created successfully. ✅
   * Try to register another account using the same username. This should fail and an error message is displayed. ✅
   * Try using a different password in the password confirmation field and confirm this fails as above. ✅

2. Testing logging in functionality.
   * Open the login page by clicking 'Sign in'. ✅
   * Attempt login using registered username and incorrect password. Should fail and an error message is displayed. ✅
   * Attempt login with a random username that doesn't exist. Verify this fails and an error message is displayed. ✅
   * Try login using a registered username and correct password. Should succeed with redirected to the main page. ✅
   * Check if log out works and then login again. ✅

3. Testing recipe functionality. Note that you need a registered account and must be logged in.
   * Try add a new recipe by clicking 'Add recipe'. Currently field values are not mandatory. After pressing 'Add' you should be redirected back to the main page. ✅
   * Try to open the recipe from the recipe list. All relevant fields should be displayed. ✅
   * Try to edit your own recipe by clicking 'Edit'. This should display the previous field values and allow you to edit them. Change some value and click 'Update'. This should redirect you back to the recipes page and update the values. ✅
   * Try to remove your own recipe by clicking 'Remove'. This should remove it and redirect you to the main page. ✅
   * Now logout and open a recipe from the list. Check that the edit and remove functionalities are not available to other users. ✅

4. You can test the search function by searching for a recipe by name without being logged in. An empty field should show all recipes.
