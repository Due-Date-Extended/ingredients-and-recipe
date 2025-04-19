from App.database import db
from .RecipeIngredient import RecipeIngredient
from .favorite import Favorite

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

  def toJSON(self):
    return{
        'id': self.id,
        'title': self.title,
        'instructions': self.instructions,
        'category': self.category,
        'image_url': self.image_url,
        'user_id': self.user_id,
        'ingredients': [recipe_ingredient.toJSON() for recipe_ingredient in self.ingredients.all()],
        'favorites': [favorite.toJSON() for favorite in self.favorites.all() ],
        'ratings': [rating.toJSON() for rating in self.ratings.all()]
    }