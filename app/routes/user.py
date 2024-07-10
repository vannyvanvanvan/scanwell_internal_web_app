from flask import Blueprint, render_template
from app.routes.login import login_required
from app.restriction import role_required

user = Blueprint('user', __name__,
                        template_folder='../templates', static_folder='../static')

@user.route('/')
@login_required
@role_required('user')
def user_dashboard():
    return render_template('user.html')