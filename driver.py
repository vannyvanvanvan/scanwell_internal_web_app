from flask import Flask
from app.routes.login import b_login
from app.routes.admin import admin
from app.routes.user import user
from app.model import User_data, db
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'b_login.login'

# Create DB
with app.app_context():
    db.create_all()
    
@login_manager.user_loader
def load_user(user_id):
    return User_data.query.get(int(user_id))


# Eegistering blueprint
app.register_blueprint(b_login)
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(user, url_prefix='/user')

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)