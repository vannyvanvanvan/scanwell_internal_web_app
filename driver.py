from datetime import timedelta
from flask import Flask
from flask_socketio import SocketIO
from app.model import db, User, Schedule, Space, Reserve, Booking
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "Thisisasecret!"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)

# Set up temporary folder for file uploads
app.config["TEMP_FOLDER"] = "%s/temp/" % app.instance_path
if not os.path.exists(app.config["TEMP_FOLDER"]):
    os.makedirs(app.config["TEMP_FOLDER"])

db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "user.user_login"

# Initialize Flask-SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Create DB if not exists
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registering blueprints
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

# Import socket events
from app.functions.socket_events import register_socket_events
register_socket_events(socketio)

if __name__ == "__main__":
    print(app.url_map)
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
