from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from app.auth.services import register_user, login_user
from app.decorators import login_required
from app.recipes.services import get_recipes, add_to_favorites, get_favorites, create_recipe, delete_recipe, \
    remove_from_favorites

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    try:
        if 'user_id' in session:
            user_id = session['user_id']
            favorites, _ = get_favorites(user_id)
            recipes, _ = get_recipes()
            return render_template('index.html', favorites=favorites, recipes=recipes)
        else:
            return render_template('index.html', favorites=[], recipes=[])
    except Exception as e:
        print(f"Error loading index page: {e}")
        flash('An error occurred.', 'danger')
        return render_template('index.html', favorites=[], recipes=[])




@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        response, status = login_user({"email": email, "password": password})
        if status == 200:
            session['user_id'] = response['user_id']  # Зберігаємо user_id в сесії
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.recipes'))
        flash(response['message'], 'danger')
    return render_template('login.html')


@main_bp.route('/recipes')
def recipes():
    try:
        recipes, _ = get_recipes()
        return render_template('recipes.html', recipes=recipes)
    except Exception as e:
        flash('An error occurred while loading recipes.', 'danger')
        return render_template('recipes.html', recipes=[])

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

@main_bp.route('/favorites/remove/<int:recipe_id>')
def remove_favorite(recipe_id):
    user_id = 1  # Симулюємо авторизованого користувача
    response, status = remove_from_favorites(user_id, recipe_id)  # Використовуємо API-сервіс
    if status == 200:
        flash('Recipe removed from favorites!', 'success')
    else:
        flash('Failed to remove recipe from favorites!', 'danger')
    return redirect(url_for('main.favorites'))

@main_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('main.login'))
