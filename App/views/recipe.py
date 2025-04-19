from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from App import db
from App.models.recipe import Recipe
from App.controllers.recipe import * #type: ignore

recipe_view = Blueprint('recipe_view', __name__)

@recipe_view.route('/recipes', methods=['GET'])
@jwt_required()
def recipes():
    #this is to query all recipes belonging to the user and render them in the recipes template 
    user_id = get_jwt_identity()
    recipes = Recipe.query.filter_by(user_id=user_id).all()
    return render_template('recipes.html', title='Recipes', recipes=recipes)

@recipe_view.route('/recipes/<int:recipe_id>', methods=['GET'])
@jwt_required()
def recipe(recipe_id):
    #this is to query a single recipe by id and render it in the recipe template
    user_id = get_jwt_identity()
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != user_id:
        flash('You do not have permission to view this recipe.', 'danger')
        return redirect(url_for('recipe_view.recipes'))
    return render_template('recipe.html', title=recipe.title, recipe=recipe)
    
@recipe_view.route('/recipes/new', methods=['POST'])
@jwt_required()
def new_recipe():
    #this isto create a new recipe for the user using form data. saves data to db and redirects them to the recipes page
    user_id = get_jwt_identity()
    title = request.form.get('title')
    instructions = request.form.get('instructions')
    category = request.form.get('category')
    image_url = request.form.get('image_url') or None

    new_recipe = create_recipe(title, instructions, category, image_url, user_id, []) #type: ignore
    flash('Your recipe has been created!', 'success')
    return redirect(url_for('recipe_view.recipes'))
    
@recipe_view.route('/recipes/update/<int:recipe_id>', methods=['POST'])
@jwt_required()
def update_recipe(recipe_id):
    #this is to update a recipe for the user using form data. saves data to db and redirects them to the recipes page
    user_id = get_jwt_identity()
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != user_id:
        flash('You do not have permission to update this recipe.', 'danger')
        return redirect(url_for('recipe_view.recipes'))

    recipe = update_recipe(recipe_id, request.form.get('title'), request.form.get('instructions'), request.form.get('category'), request.form.get('image_url') or None, [])
    
    flash('Your recipe has been updated!', 'success')
    return redirect(url_for('recipe_view.recipes'))
    

@recipe_view.route('/recipes/delete/<int:recipe_id>', methods=['POST'])
@jwt_required()
def delete_recipe(recipe_id):
    #this is to delete a recipe for the user. deletes data from db and redirects them to the recipes page
    user_id = get_jwt_identity()
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != user_id:
        flash('You do not have permission to delete this recipe.', 'danger')
        return redirect(url_for('recipe_view.recipes'))

    delete_recipe(recipe_id)
    flash('Your recipe has been deleted!', 'success')
    return redirect(url_for('recipe_view.recipes'))

@recipe_view.route('/recipes/search', methods=['GET'])
@jwt_required()
def search_recipes():
    #this is to search for recipes by title or category
    user_id = get_jwt_identity()
    if user_id is None:
        flash('You must be logged in to search for recipes.', 'danger')
        return redirect(url_for('auth_views.login_action'))

    query = request.args.get('query')
    recipes = fetch_api_recipes(query) #type: ignore
    
    return render_template('recipes.html', title='Recipes', recipes=recipes)