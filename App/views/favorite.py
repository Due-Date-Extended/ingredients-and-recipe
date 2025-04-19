from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from App import db
from App.models import Favorite
from App.controllers import * #type: ignore

favorite_view = Blueprint('favorite_view', __name__)

@favorite_view.route('/favorites', methods=['GET'])
@jwt_required()
def get_favorites():
    #this is to query the db for the user's favorite recipes and render them in the favorites template
    user_id = get_jwt_identity()
    get_all_favorites_by_user(user_id) #type: ignore
    return render_template('favorites.html', favorites=favorites)

@favorite_view.route('/favorites/add/<int:recipe_id>', methods=['POST'])
@jwt_required()
def add_favorite(recipe_id):
    #this is to add a recipe to the user's favorites. adds the favorite to the db and redirects to the favorites page
    user_id = get_jwt_identity()
    create_favorite(user_id, recipe_id) #type: ignore
    flash('Recipe added to favorites!', 'success')
    return redirect(url_for('favorite_view.get_favorites'))

@favorite_view.route('/favorites/remove/<int:recipe_id>', methods=['POST'])
@jwt_required()
def remove_favorite(recipe_id):
    #this is to remove a recipe from the user's favorites. removes the favorite from the db and redirects to the favorites page
    user_id = get_jwt_identity()
    remove_favorite(user_id, recipe_id)
    flash('Recipe removed from favorites!', 'success')
    return redirect(url_for('favorite_view.get_favorites'))

