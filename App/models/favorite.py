from App.database import db
from datetime import datetime, timezone

class Favorite(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

  def __init__(self, user_id, recipe_id):
      self.user_id = user_id
      self.recipe_id = recipe_id
      self.date_added = datetime.now(timezone.utc)
      self.recipes = []
    
  def get_json(self):
    return{
        'id': self.id,
        'recipe_id': self.recipe_id,
        'user_id': self.user_id
    }
