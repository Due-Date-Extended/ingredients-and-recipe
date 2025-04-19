from App.models.rating import Rating
from App.database import db

def create_rating(user_id, recipe_id, score):
    new_rating = Rating(user_id=user_id, recipe_id=recipe_id, score=score)
    db.session.add(new_rating)
    db.session.commit()
    return new_rating

def get_rating(id):
    return Rating.query.get(id)

def delete_rating(id):
    rating = get_rating(id)
    if rating:
        db.session.delete(rating)
        return db.session.commit()
    return None


def update_rating(rating, score):
    rating.score = score
    db.session.add(rating)
    return db.session.commit()
