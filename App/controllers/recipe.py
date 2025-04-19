from App.models.recipe import Recipe
from App.models.RecipeIngredient import RecipeIngredient
from App.database import db
from flask import requests
import json


def create_recipe(title, instructions, category, image_url, user_id, ingredients):
    new_recipe = Recipe(title=title,instructions=instructions, category=category, image_url=image_url, user_id=user_id)
    db.session.add(new_recipe)
    if ingredients:
     for ingredient in ingredients:
        new_recipe.add_ingredient(ingredient['ingredient'], ingredient['quantity'], ingredient['unit'])
    #db.session.commit()
    #return new_recipe
    db.session.add(new_recipe)
    db.session.flush()
    db.session.commit()
    return new_recipe

def get_recipe(id):
    return Recipe.query.get(id)

def get_all_recipes():
    return Recipe.query.all()

def update_recipe(id, title, instructions, category, image_url, ingredients):
    recipe = get_recipe(id)
    if recipe:
        recipe.title = title
        recipe.instructions = instructions
        recipe.category = category
        recipe.image_url = image_url
        if ingredients:
            recipe.ingredients = []
            for ingredient in ingredients:
                recipe.add_ingredient(ingredient['ingredient'], ingredient['quantity'], ingredient['unit'])
        db.session.add(recipe)
        return db.session.commit()
    return None

def delete_recipe(id):
    recipe = get_recipe(id)
    if recipe:
        db.session.delete(recipe)
        return db.session.commit()
    return None

def get_recipes_by_user(user_id):
    return Recipe.query.filter_by(user_id=user_id).all()

def add_ingredient_to_recipe(recipe_id, ingredient, quantity, unit):
    recipe = get_recipe(recipe_id)
    if recipe:
        recipe.add_ingredient(ingredient, quantity, unit)
        return recipe
    return None 

def get_recipes_by_ingredient(ingredient_id):
    return Recipe.query.join(RecipeIngredient).filter(RecipeIngredient.ingredient_id == ingredient_id).all()  # type: ignore  

def get_recipes_by_category(category):
    return Recipe.query.filter_by(category=category).all()

def get_recipes_by_title(title):
    return Recipe.query.filter(Recipe.title.ilike(f'%{title}%')).all() #type: ignore

def favorite_recipe(user_id, recipe_id):
    recipe = get_recipe(recipe_id)
    if recipe:
        recipe.add_favorite(user_id)
        return recipe
    return None

def unfavorite_recipe(user_id, recipe_id):
    recipe = get_recipe(recipe_id)
    if recipe:
        recipe.remove_favorite(user_id)
        return recipe
    return None

def rate_recipe(user_id, recipe_id, score):
    recipe = get_recipe(recipe_id)
    if recipe:
        recipe.add_rating(user_id, score)
        return recipe
    return None

def fetch_api_recipes(search_term):
    url = f'https://www.themealdb.com/api/json/v1/1/search.php?s={search_term}'
    response = requests.get(url)
    if response.status_code != 200:
        print('Error fetching recipes from API')
        return []

    data = response.json()

    recipes = []
    for meal in data.get('meals', []):
        recipe = {
            'title': meal['strMeal'],
            'instructions': meal['strInstructions'],
            'category': meal['strCategory'],
            'image_url': meal['strMealThumb'],
            'ingredients': []
        }
        for i in range(1, 21):
            ingredient = meal[f'strIngredient{i}']
            measure = meal[f'strMeasure{i}']
            if ingredient:
                recipe['ingredients'].append({'ingredient': ingredient, 'measure': measure})
        recipes.append(recipe)
        db.session.add(recipe)
        db.session.commit()
    
    return recipes
    
def search_recipes(search_term):
    recipes = get_recipes_by_title(search_term)
    if not recipes:
        recipes = fetch_api_recipes(search_term)
        return recipes
    return recipes
    




