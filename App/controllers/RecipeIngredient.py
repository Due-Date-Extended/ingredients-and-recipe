from App.models.RecipeIngredient import RecipeIngredient
from App.database import db

def create_recipe_ingredient(recipe_id, ingredient_id, quantity, unit):
    new_recipe_ingredient = RecipeIngredient(recipe_id=recipe_id, ingredient_id=ingredient_id, quantity=quantity, unit=unit)
    db.session.add(new_recipe_ingredient)
    db.session.commit()
    return new_recipe_ingredient

def missing_recipe_ingredient(recipe_id, ingredient_id):
    recipe_ingredient = RecipeIngredient.query.filter_by(recipe_id=recipe_id, ingredient_id=ingredient_id).first()
    if recipe_ingredient:
        return recipe_ingredient  