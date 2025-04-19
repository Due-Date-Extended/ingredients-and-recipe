from flask import Blueprint, request, redirect, url_for, flash
from flask_jwt_extended import get_jwt_identity, jwt_required
from App.models.rating import Rating
from App.controllers.rating import create_rating, update_rating, delete_rating

rating_view = Blueprint('rating_view', __name__, template_folder='../templates')

@rating_view.route('/ratings/new/<int:recipe_id>', methods=['POST'])
@jwt_required()
def rating(recipe_id):
  user_id = get_jwt_identity()
  score = request.form.get('score')
  if not score:
    flash('Please provide a rating score.', 'danger')
    return redirect(url_for('recipe_views.get_recipe', id=recipe_id))

  if not score.isdigit() or int(score) < 1 or int(score) > 5:
    flash('Please provide a valid rating score between 1 and 5.', 'danger')
    return redirect(url_for('recipe_views.get_recipe', id=recipe_id))

  create_rating(user_id, recipe_id, score)
  flash('Your rating has been added!', 'success')
  return redirect (url_for('recipe_views.get_recipe', id=recipe_id))  


@rating_view.route('/ratings/delete/<int:id>', methods=['POST'])
@jwt_required()
def deleteRating(id):
  rating = Rating.query.get_or_404(id)
  if rating.user_id != get_jwt_identity():
    flash('You do not have permission to delete this rating.', 'danger')
    return redirect(url_for('recipe_views.get_recipe', id=rating.recipe_id))
    
  delete_rating(rating)
  flash('Your rating has been deleted!', 'success')
  return redirect(url_for('recipe_views.get_recipe', id=rating.recipe_id))


@rating_view.route('/ratings/update/<int:id>', methods=['POST'])
@jwt_required()
def updateRating(id):
  rating = Rating.query.get_or_404(id)
  if rating.user_id != get_jwt_identity():
    flash('You do not have permission to update this rating.', 'danger')
    return redirect(url_for('recipe_views.get_recipe', id=rating.recipe_id))

  score = request.form.get('score')
  if not score:
    flash('Please provide a rating score.', 'danger')
    return redirect(url_for('recipe_views.get_recipe', id=rating.recipe_id))

  if not score.isdigit() or int(score) < 1 or int(score) > 5:
    flash('Please provide a valid rating score between 1 and 5.', 'danger')
    return redirect(url_for('recipe_views.get_recipe', id=rating.recipe_id))

  update_rating(rating, score)
  flash('Your rating has been updated!', 'success')
  return redirect(url_for('recipe_views.get_recipe', id=rating.recipe_id))