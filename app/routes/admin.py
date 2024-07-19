from flask import Blueprint, render_template
from app.routes.login import login_required
from app.restriction import role_required

admin = Blueprint('admin', __name__,
                  template_folder='../templates', static_folder='../static')


@admin.route('/')
@login_required
@role_required('admin')
def admin_dashboard():
    return render_template('admin.html')
