from flask import Flask
from app.model import db, User, Schedule, Space, Reserve, Booking
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "Thisisasecret!"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

# Set up temporary folder for file uploads
app.config["TEMP_FOLDER"] = "%s/temp/" % app.instance_path
# Create temp folder on local disk if folder doesn't exist
if not os.path.exists(app.config["TEMP_FOLDER"]):
    os.makedirs(app.config["TEMP_FOLDER"])

# from app.routes.login import b_login
# from app.routes.admin import admin
# from app.routes.user import user
from app.routes.user import user

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


# # Eegistering blueprint
# app.register_blueprint(b_login)
# app.register_blueprint(admin, url_prefix="/admin")
# app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(user)

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)
