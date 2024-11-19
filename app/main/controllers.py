from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from app.auth.services import register_user, login_user
from app.decorators import login_required
from app.recipes.models import TriedRecipe
from app.recipes.services import get_recipes, add_to_favorites, get_favorites, create_recipe, delete_recipe, \
    remove_from_favorites, filter_recipes

from app.auth.models import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    try:
        if 'user_id' in session:
            user_id = session['user_id']
            favorites, _ = get_favorites(user_id)  # Отримання улюблених
            recipes, _ = get_recipes()  # Отримання всіх рецептів
            return render_template('index.html', favorites=favorites, recipes=recipes)
        else:
            return render_template('index.html')
    except Exception as e:
        print(f"Error loading index page: {e}")
        flash('An error occurred.', 'danger')
        return render_template('index.html')




@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        response, status = login_user({"email": email, "password": password})
        if status == 200:
            session['user_id'] = response['user_id']
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.index'))
        flash(response.get('message', 'Login failed!'), 'danger')
    return render_template('login.html')



@main_bp.route('/recipes')
def recipes():
    if 'user_id' in session:
        user_id = session['user_id']
        tried_recipes = {entry.recipe_id for entry in TriedRecipe.query.filter_by(user_id=user_id).all()}
    else:
        tried_recipes = set()

    recipes, _ = get_recipes()
    return render_template('recipes.html', recipes=recipes, tried_recipes=tried_recipes)


@main_bp.route('/favorites/add/<int:recipe_id>')
def add_favorite(recipe_id):
    if 'user_id' not in session:
        flash('You need to log in to add favorites.', 'danger')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    response, status = add_to_favorites(user_id, recipe_id)
    if status == 201:
        flash('Recipe added to favorites!', 'success')
    else:
        flash(response['message'], 'danger')
    return redirect(url_for('main.recipes'))



@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        response, status = register_user({"email": email, "password": password})
        if status == 201:
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('main.login'))
        else:
            flash(response['message'], 'danger')
    return render_template('register.html')



@main_bp.route('/favorites')
@login_required
def favorites():
    user_id = 1  # Симулюємо авторизованого користувача
    favorites, _ = get_favorites(user_id)  # Використовуємо API-сервіс
    return render_template('favorites.html', favorites=favorites)

@main_bp.route('/recipes/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        try:
            data = {
                "title": request.form['title'],
                "description": request.form['description'],
                "steps": request.form['steps'],
                "time_to_cook": int(request.form['time_to_cook']),
                "servings": int(request.form['servings']),
                "ingredients": request.form['ingredients'].split(',')
            }
            response, status = create_recipe(data)
            if status == 201:
                flash('Recipe added successfully!', 'success')
                return redirect(url_for('main.recipes'))
            flash('Failed to add recipe!', 'danger')
        except Exception as e:
            flash('An error occurred while adding the recipe.', 'danger')
    return render_template('add_recipe.html')


@main_bp.route('/recipes/remove/<int:recipe_id>')
def remove_recipe(recipe_id):
    response, status = delete_recipe(recipe_id)  # Використовуємо сервіс API
    if status == 200:
        flash('Recipe deleted successfully!', 'success')
    else:
        flash('Failed to delete recipe!', 'danger')
    return redirect(url_for('main.recipes'))

@main_bp.route('/favorites/remove/<int:recipe_id>', methods=['POST'])
def remove_favorite_ui(recipe_id):
    """Видаляє рецепт із улюблених через Web UI."""
    if 'user_id' not in session:
        flash("You need to log in to perform this action.", "danger")
        return redirect(url_for('main.index'))

    user_id = session['user_id']
    response, status = remove_from_favorites(user_id, recipe_id)

    if status == 200:
        flash("Recipe removed from favorites.", "success")
    else:
        flash(response.get("message", "An error occurred."), "danger")
    return redirect(url_for('main.index'))

@main_bp.route('/logout')
def logout():
    session.pop('user_id', None)  # Видаляємо user_id із сесії
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))

@main_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('You need to log in to access your profile.', 'danger')
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    user = User.query.get(user_id)  # Отримання даних користувача з бази

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('main.index'))

    return render_template('profile.html', user=user)

@main_bp.route('/search', methods=['GET', 'POST'])
def search_recipes():
    recipes = []
    filters = {"ingredients": [], "max_time": None, "search": None}

    if request.method == 'POST':
        filters.update({
            "ingredients": request.form.get('ingredients', '').split(','),
            "max_time": request.form.get('max_time'),
            "search": request.form.get('search')
        })

        # Видаляємо порожні значення
        filters['ingredients'] = [i.strip() for i in filters['ingredients'] if i.strip()]
        recipes, _ = filter_recipes(filters)

    return render_template('search.html', recipes=recipes, filters=filters)




