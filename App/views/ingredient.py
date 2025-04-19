from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from App import db
from App.models.ingredient import Ingredient
from App.controllers.ingredient import * #type: ignore

ingredient_view = Blueprint('ingredient_view', __name__, template_folder='../templates')

@ingredient_view.route('/inventory', methods=['GET'])
@jwt_required()
def get_inventory():
    #this is to query the db for the user's ingredients and render them in the inventory template
    user_id = get_jwt_identity()
    ingredients = Ingredient.query.filter_by(user_id=user_id).all()
    return render_template('inventory.html', ingredients=ingredients)


@ingredient_view.route('/inventory/add', methods=['POST'])
@jwt_required()
def add_ingredient():
  #this is to add a new ingredient using the form data. adds the ingredient to the db and redirects to the inventory page
  user_id = get_jwt_identity()
  name = request.form['name']
  quantity = request.form['quantity']
  unit = request.form['unit']
  expiration_date = request.form['expiration_date'] or None

  ingredient = create_ingredient(user_id, name, quantity, unit, expiration_date) #type: ignore
    
  flash('Ingredient added successfully!', 'success')
  return redirect(url_for('ingredient_views.get_inventory'))
  #return render_template('inventory.html', ingredients=ingredients)


@ingredient_view.route('/inventory/update/<int:id>', methods=['POST'])
@jwt_required()
def update_ingredient(id):
  #this is to edit an existing ingredient using the form data. updates the ingredient in the db and redirects to the inventory page
    user_id = get_jwt_identity()
    ingredient = get_ingredient(id) #type: ignore
    if not ingredient or ingredient.user_id != user_id:
        flash('You do not have permission to edit this ingredient.', 'danger')
        return redirect(url_for('ingredient_views.get_inventory'))
    try:
          ingredient = update_ingredient(id, request.form['name'],     request.form['quantity'], request.form['unit'], request.form['expiration_date'] or None)
          flash('Ingredient updated successfully!', 'success')
    except Exception as e:
          flash(f'Error updating ingredient: {str(e)}', 'danger')
    return redirect(url_for('ingredient_view.get_inventory'))
  


@ingredient_view.route("/inventory/delete/<int:id>", methods=['POST'])
@jwt_required()
def delete_ingredient(id):
#this removes an ingredient beloning to the user from the db and redirects to the inventory page
    user_id = get_jwt_identity()
    ingredient = get_ingredient(id)    #type: ignore
    if not ingredient or ingredient.user_id != user_id:
      flash('You do not have permission to delete this ingredient.', 'danger')
      return redirect(url_for('ingredient_views.get_inventory'))
    
    delete_ingredient(id)
    
    flash('Ingredient deleted successfully!', 'success')
    return redirect(url_for('ingredient_views.get_inventory'))