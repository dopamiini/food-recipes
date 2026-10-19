## Testing the Application

The application can be tested manually by following the checklist below. These tests cover the main functionalities of the application, including user registration, authentication, recipe management, ratings, comments, image uploads, search, and navigation. This is mostly fairly intuitive. Here's a coverage of successful test cases.

### 1. Testing user registration

- Open the registration page by clicking **Register**.
- Register a new account and verify that it is created successfully.
- There is no enforcement for password complexity or rate limiting, as it is easier to test the app this way.
- Try submitting a registration form with invalid or missing information in some combination and verify that appropriate validation errors are displayed. For example, registering another account with the same username should fail and display an error message.

### 2. Testing login and logout

- Open the login page by clicking **Sign in**.
- Try logging in with the registered username and paswword, this should succeed.
- Try logging in with any combination of invalid or missing information and verify that appropriate validation errors are displayed. For example, a username that doesn't exist.
- Also, later logout and verify that you are unable to access user specific functionality that was available to you while you were logged in with a registered account once you create recipes, etc.

### 3. Testing recipe creation

*You must be logged in to create recipes.*

- Open the recipe creation page by clicking **Add recipe**.
- Enter the recipe title, description, ingredients, instructions, and categories. Click Add recipe. You should be redirected to the main page and your recipe is now added.
- Try submitting missing, invalid or excessively long inputs and verify that server-side validation works as expected.

### 4. Testing recipe viewing and navigation

- Click on a recipe title or image from the recipe list and verify that you can access the recipe's detailed page.
- Use the available navigation links and buttons to verify that they lead to 'appropriate' pages.
- You can create a second account and verify that the application enforces server-side access restrictions to pages that you are not supposed to be able to visit. 

### 5. Testing recipe editing and deletion

*You must be logged in and own the recipe to edit or delete it.*

- Open one of your own recipes and click **Edit**.
- Verify that the existing recipe information is displayed in the form.
- Change some information and save the changes. Verify that the updated information is displayed correctly.
- Try submitting a recipe that has some fields empty and note that server-side validation is enforced.
- Log in as another user and verify that you cannot edit or delete recipes belonging to someone else.
- Delete your own recipe and verify that it disappears from the recipe list. You can also check the database.

### 6. Testing recipe images

*You must be logged in and own the recipe to edit or delete associated image files.*

- Navigate to the individual recipe page by clicking on the title or picture of a recipe that you own.
- Upload a valid PNG image of 5 MB or less and verify that it is displayed correctly with the recipe.
- Replace an existing image with another image and verify that the new image is displayed.
- Remove the image and verify that the default image is displayed.
- Try uploading an invalid file type or an image exceeding the allowed size and verify that the upload is rejected. The PNG validation is not very robust, but it should block other normal files of different formats.

### 7. Testing recipe ratings

- Navigate to the recipe page of any recipe and submit a rating. Verify that the rating is saved and displayed correctly.
- Verify a user can only rate a single recipe once.
- Change or delete your rating and verify that the updated rating is reflected.

### 8. Testing recipe comments

- Navigate to the recipe page and submit a comment. Verify that the comment is saved and displayed correctly.
- Try submitting multiple comments.
- Try submitting an empty or excessively long comment and verify that the application handles it according to its validation rules.
- Verify that comments are associated with the correct user and recipe.
- Check that user-submitted text is displayed safely and that HTML or JavaScript entered as text is not executed.
- Test editing and removing comments.
- Empty comments should give an error message.

### 9. Testing recipe search

- Search for a recipe by its title or a relevant keyword and verify that matching recipes are displayed.
- Search for a term that does not match any recipes and verify that an appropriate empty result is displayed.
- Submit an empty search field and verify that all recipes are displayed.
- Try searching for recipes by selecting only categories and entering a search term in the search field.
- Test searching while logged out to verify that public recipe browsing works similarly.

### 10. Testing Access Control and Security

- Verify that creating, editing, deleting, rating, and commenting requires authentication.
- Verify that users cannot modify or delete another user's recipes by accessing a URL directly.
- Submit forms without a valid CSRF token and verify that the requests are rejected.
- Enter unusual or malicious-looking text into form fields and verify that input validation and output escaping work correctly.
