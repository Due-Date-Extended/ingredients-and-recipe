# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .favorite import favorite_view
from .ingredient import ingredient_view
from .recipe import recipe_view
from .rating import rating_view


#from .admin import setup_admin


views = [user_views, index_views, auth_views, favorite_view, ingredient_view, recipe_view, rating_view] 
# blueprints must be added to this list