#import os
from flask import Flask, render_template
from flask_uploads import DOCUMENTS,IMAGES, TEXT, UploadSet, configure_uploads
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
from threading import Lock
from App.controllers.user import * #type: ignore
from App.controllers.ingredient import get_ingredients_expiring_today
from App.models import User
#from werkzeug.utils import secure_filename
#from werkzeug.datastructures import  FileStorage


from App.database import init_db
from App.config import load_config


from App.controllers import (
    setup_jwt,
    add_auth_context
)

from App.views import views
from App.views.admin import setup_admin

thread = None
thread_lock = Lock()

def add_views(app): 
    for view in views:
        app.register_blueprint(view)

def create_app(overrides={}):
    app = Flask(__name__, static_url_path='/static')
    load_config(app, overrides)
    CORS(app)
    add_auth_context(app)
    photos = UploadSet('photos', TEXT + DOCUMENTS + IMAGES)
    configure_uploads(app, photos)
    socketio = SocketIO(app, cors_allowed_origins= "*")   
    

    add_views(app)
    init_db(app)
    jwt = setup_jwt(app)
    setup_admin(app)

    @jwt.invalid_token_loader
    @jwt.unauthorized_loader
    def custom_unauthorized_response(error):
        return render_template('401.html', error=error), 401

    # from here 

    #this is to send a notification to the user when an ingredient is expiring today
    def background_thread():
        with app.app_context():
            while True:
                users = get_all_users() #type: ignore
                for user in users:
                    expiring_ingredients = get_ingredients_expiring_today(user.id)
                    for ingredient in expiring_ingredients:
                        socketio.emit('expiration_alert', {
                                          'message': f"Ingredient {ingredient.name} expires today!",
                                          'ingredient_id': ingredient.id,
                                          'user_id': user.id
                                      }, namespace='/notifications')
                socketio.sleep(60*60)

    @socketio.on('connect', namespace='/notifications')
    def connect():
        global thread
        with thread_lock:
            if thread is None:
                thread = socketio.start_background_task(background_thread)
        emit('Connected', {'data': 'Connected to notifications'})

    @socketio.on('join', namespace='/notifications')
    def on_join(data):
        user_id = data['user_id']
        join_room(str(user_id))
        emit('joined', {'data': f'Joined room for user {user_id}'})


    app.app_context().push()
    app.socketio = socketio # type: ignore
    return app
