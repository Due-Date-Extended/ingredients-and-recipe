from App.models.ingredient import Ingredient
from App.database import db
from datetime import datetime

def create_ingredient(user_id, name, quantity, unit, expiration_date):
    new_ingredient = Ingredient(user_id=user_id, name=name, quantity=quantity, unit=unit, expiration_date=expiration_date)
    db.session.add(new_ingredient)
    db.session.commit()
    return new_ingredient 

def get_ingredient(id):
    return Ingredient.query.get(id)

def get_all_ingredients():
    return Ingredient.query.all()

def update_ingredient(id, name, quantity, unit, expiration_date):
    ingredient = get_ingredient(id)
    if ingredient:
        ingredient.name = name
        ingredient.quantity = quantity
        ingredient.unit = unit
        ingredient.expiration_date = expiration_date
        db.session.add(ingredient)
        return db.session.commit()
    return None

def delete_ingredient(id):
    ingredient = get_ingredient(id)
    if ingredient:
        db.session.delete(ingredient)
        return db.session.commit()
    return None

def get_ingredients_by_user(user_id):
    return Ingredient.query.filter_by(user_id=user_id).all()

def add_ingredient_to_recipe(ingredient_id, recipe_id):
    ingredient = get_ingredient(ingredient_id)
    if ingredient:
        ingredient.add_recipe(recipe_id)
        return ingredient
    return None

def get_ingredients_expiring_today(user_id):
    today = datetime.now().date()
    return Ingredient.query.filter_by(user_id=user_id, expiration_date=today).all()



