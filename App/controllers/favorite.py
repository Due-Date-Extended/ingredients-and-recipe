from App.models.favorite import Favorite
from App.database import db

def create_favorite(user_id, recipe_id):
    new_favorite = Favorite(user_id=user_id, recipe_id=recipe_id)
    db.session.add(new_favorite)
    db.session.commit()
    return new_favorite

def remove_favorite(user_id, recipe_id):
    favorite = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return True
    return False

def update_favorite(user_id, recipe_id):
    favorite = Favorite.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    if favorite:
        db.session.add(favorite)
        db.session.commit()
        return favorite
    return None

def get_favorite(id):
    return Favorite.query.get(id)

def get_all_favorites_by_user(user_id):
    return Favorite.query.filter_by(user_id=user_id).all()

      