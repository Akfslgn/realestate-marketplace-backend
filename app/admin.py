from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.extensions import db
from app.models.example import User

admin_panel = Admin(name='Admin Panel', template_mode='bootstrap4')

def init_admin(app):
    admin_panel.init_app(app)
    admin_panel.add_view(ModelView(User, db.session))
    return admin_panel