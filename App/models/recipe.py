from App.database import db
from .RecipeIngredient import RecipeIngredient
from .favorite import Favorite
from .rating import Rating

class Recipe(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  instructions = db.Column(db.Text, nullable=False)
  category = db.Column(db.String(200), nullable=True)
  image_url = db.Column(db.String(200), nullable=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  ingredients = db.relationship('RecipeIngredient', backref='recipe', lazy='joined')
  favorites = db.relationship('Favorite', backref='recipe', lazy=True)
  ratings = db.relationship('Rating', backref='recipe', lazy=True)

  def __init__(self, title, instructions, category, image_url, user_id):
      self.title = title
      self.instructions = instructions
      self.category = category
      self.image_url = image_url
      self.user_id = user_id

  def add_ingredient(self, ingredient, quantity, unit):
    recipe_ingredient = RecipeIngredient(recipe_id=self.id, ingredient_id=ingredient.id, quantity=quantity, unit=unit)
    self.ingredients.append(recipe_ingredient)
    db.session.add(recipe_ingredient)
    db.session.commit()
    return self

  def add_favorite(self, user):
    favorite = Favorite(user_id=user.id, recipe_id=self.id)
    self.favorites.append(favorite)
    db.session.add(favorite)
    db.session.commit()
    return self

  def remove_favorite(self, user):
    favorite = Favorite.query.filter_by(user_id=user.id, recipe_id=self.id).first()
    if favorite:
      db.session.delete(favorite)
      db.session.commit()
      return self
    return None

  
  def get_json(self):
    return{
        'id': self.id,
        'title': self.title,
        'instructions': self.instructions,
        'category': self.category,
        'image_url': self.image_url,
        'user_id': self.user_id,
        'ingredients': [recipe_ingredient.get_json() for recipe_ingredient in self.ingredients.all()],
        'favorites': [favorite.get_json() for favorite in self.favorites.all() ],
        'ratings': [rating.get_json() for rating in self.ratings.all()]
    }

  def add_rating(self, user, score):
    rating = Rating(user_id=user.id, recipe_id=self.id, score=score)
    self.ratings.append(rating)
    db.session.add(rating)
    db.session.commit()
    return self

  def remove_rating(self, user):
    rating = Rating.query.filter_by(user_id=user.id, recipe_id=self.id).first()
    if rating:
      db.session.delete(rating)
      db.session.commit()
      return self
    return None


  def missing_ingredients(self, user):
    missing = []
    for recipe_ingredient in self.ingredients: #type: ignore
      ingredient = recipe_ingredient.ingredient
      user_ingredient = user.ingredients.filter_by(id=ingredient.id).first()
      if not user_ingredient or user_ingredient.quantity < recipe_ingredient.quantity:
        missing.append(recipe_ingredient)
        return missing
      return None


  