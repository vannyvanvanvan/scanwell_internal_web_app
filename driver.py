from flask_socketio import SocketIO
from flask import Flask
from app.model import db, User, Schedule, Space, Reserve, Booking
from flask_login import LoginManager
import os

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Thisisasecret!!!"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

    # Set up temporary folder for file uploads
    app.config["TEMP_FOLDER"] = "%s/temp/" % app.instance_path
    # Create temp folder on local disk if folder doesn't exist
    if not os.path.exists(app.config["TEMP_FOLDER"]):
        os.makedirs(app.config["TEMP_FOLDER"])


    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.user_login"

    # Create DB
    with app.app_context():
        db.create_all()


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Registering blueprint
    from app.routes.user import user_routes
    from app.routes.schedule import schedule_routes
    from app.routes.space import space_routes
    from app.routes.reserve import reserve_routes
    from app.routes.booking import booking_routes
    from app.routes.search import search_routes

    from app.routes.admin import admin_routes
    app.register_blueprint(user_routes)
    app.register_blueprint(schedule_routes, url_prefix="/schedule")
    app.register_blueprint(space_routes, url_prefix="/space")
    app.register_blueprint(reserve_routes, url_prefix="/reserve")
    app.register_blueprint(booking_routes, url_prefix="/booking")
    app.register_blueprint(search_routes, url_prefix="/search")

    app.register_blueprint(admin_routes, url_prefix="/admin")

    # Initialize SocketIO
    socketio.init_app(app, cors_allowed_origins="*")
    
    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    print(app.url_map)
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
