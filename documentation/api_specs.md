
# Recipe Finder - API Endpoints

## 1. Recipes (`/recipes`)

### **GET /recipes/**
**Description:** Get a list of all recipes.

---

### **POST /recipes/**
**Description:** Add a new recipe.  
**Request Body:**
```json
{
  "title": "string",
  "description": "string",
  "steps": "string",
  "time_to_cook": "integer",
  "servings": "integer",
  "ingredients": ["string"]
}
```

---

### **DELETE /recipes/<int:recipe_id>**
**Description:** Delete a recipe by its ID.

---

### **POST /recipes/tried/<int:recipe_id>**
**Description:** Mark a recipe as "tried".

---

### **GET /recipes/random**
**Description:** Get a random recipe ("I'm Feeling Hungry").

---

### **GET /recipes/favorites**
**Description:** Get a list of the user's favorite recipes.

---

### **POST /recipes/favorites**
**Description:** Add a recipe to favorites.  
**Request Body:**
```json
{
  "recipe_id": "integer"
}
```

---

### **DELETE /recipes/favorites/<int:recipe_id>**
**Description:** Remove a recipe from favorites.

---

## 2. Authentication (`/auth`)

### **POST /auth/register**
**Description:** Register a new user.  
**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

---

### **POST /auth/login**
**Description:** Log in a user using JWT.  
**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

---

### **POST /auth/logout**
**Description:** Log out a user (invalidate token).

---

### **GET /auth/me**
**Description:** Get information about the current user.

---

## 3. Profile (`/profile`)

### **GET /profile/**
**Description:** Get details of the current user's profile.

---

### **PUT /profile/**
**Description:** Update user profile information.  
**Request Body:**
```json
{
  "email": "string",
  "name": "string"
}
```

---

## 4. Admin Panel (`/admin`)

### **GET /admin/recipes**
**Description:** Get a list of all recipes (admin only).

---

### **GET /admin/users**
**Description:** Get a list of all users (admin only).

---

### **DELETE /admin/users/<int:user_id>**
**Description:** Delete a user by their ID (admin only).

---

## Notes
- All routes are protected with **JWT Authentication** where applicable.
- Admin routes require the user to have administrator privileges.