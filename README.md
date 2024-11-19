# Recipe Finder - Functional Requirements

## Project Name
**Recipe Finder**

## Idea
This is a web application where users can input available ingredients, and the app suggests recipes they can prepare.

---

## Functional Requirements

### 1. Input Ingredients
**Main Functionality:**
- Users can input a list of ingredients via a text field (e.g., "egg, milk, flour").

**Additional Features:**
- A list of frequently used ingredients for quick selection (e.g., "milk", "eggs").
- Autocomplete ingredients during input (based on the database of ingredients).

**Validation:**
- Verify that the entered ingredients exist in the database.
- Warn if non-existent ingredients are entered.

---

### 2. Recipe Search
**Main Functionality:**
- The app analyzes the list of ingredients and suggests recipes that use all or some of them.

**Additional Features:**
- Filter results by:
  - Category (desserts, soups, main dishes, etc.).
  - Cooking time.
  - Number of ingredients in the recipe.
- Sort by popularity, rating, or cooking time.

**Validation:**
- If no recipes match the entered ingredients, suggest the most similar options.

---

### 3. User Registration (Optional)
**Main Functionality:**
- Registration via email and password.
- Login using JWT.

**Additional Features:**
- Login via Google/Facebook (optional for the first version).

**Validation:**
- Ensure the email is unique.
- Enforce password complexity.

**Special Features:**
- Guest mode for searching recipes without registration.

---

### 4. Save Favorite Recipes (For Registered Users)
**Main Functionality:**
- Users can save recipes to a personal collection.

**Additional Features:**
- Mark recipes as "tried".
- Sort favorite recipes by category.

**Special Features:**
- Limit the number of favorite recipes for guest users (e.g., 3 recipes).

---

### 5. Admin Panel
**Main Functionality:**
- The admin can:
  - Add new recipes.
  - Edit existing recipes.
  - Delete recipes.

**Additional Features:**
- Bulk upload recipes via file (CSV/JSON).
- Display usage statistics for recipes:
  - Most popular recipes.
  - Most searched ingredients.

---

### 6. Recipe Details
**Main Functionality:**
- Display the full recipe details:
  - Title.
  - List of ingredients.
  - Cooking steps.
  - Cooking time.
  - Number of servings.

**Additional Features:**
- Image of the finished dish.
- Link to a video tutorial (if available).
- Recipe rating (with the ability to vote).

---

### 7. Random Recipe ("I'm Feeling Hungry")
**Main Functionality:**
- Random recipe selection from the general database.

**Additional Features:**
- Recommendations based on the user's recent searches.

---

### 8. Security
**Basic:**
- Use JWT to secure API endpoints.
- Input sanitization to prevent SQL injection.

**Advanced:**
- Rating system for reviews with validation (to prevent spam).
- Role-based access control (user/admin).

---
