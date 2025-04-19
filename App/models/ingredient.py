from App.database import db
from datetime import datetime, timezone

class Ingredient(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  name = db.Column(db.String(100), nullable=False)
  quantity = db.Column(db.Float, nullable=False, default=0.0)
  unit = db.Column(db.String(20), nullable=True)
  expiration_date = db.Column(db.Date, nullable=True, index=True)
  date_added = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc), index=True)
  recipes = db.relationship('RecipeIngredient', backref='ingredient', lazy='joined')

  def __init__(self, user_id, name, quantity, unit, expiration_date):
    self.user_id = user_id
    self.name = name
    self.quantity = quantity
    self.unit = unit
    self.expiration_date = expiration_date
    self.date_added = datetime.now(timezone.utc)
    #self.recipes = []

  def add_recipe(self, recipe):
    self.recipes.append(recipe)
    recipe.ingredients.append(self)
    db.session.add(self)
    db.session.add(recipe)
    db.session.commit()
    return self

  def get_json(self):
    return{
        'id': self.id,
        'user_id': self.user_id,
        'name': self.name,
        'quantity': self.quantity,
        'unit': self.unit,
        'expiration_date': self.expiration_date,
        'date_added': self.date_added,
        'recipes': [recipe_ingredient.get_json() for recipe_ingredient in self.recipes.all() ]} 