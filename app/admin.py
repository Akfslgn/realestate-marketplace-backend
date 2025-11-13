from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.extensions import db
from app.models import Listing, ListingImage, Profile, User, WishlistItem

admin_panel = Admin(name="HomeHeaven Admin Panel")


class UserView(ModelView):
    column_list = [c.name for c in User.__table__.columns if not c == "password"]
    form_columns = [c.name for c in User.__table__.columns]  # type: ignore


class ProfileView(ModelView):
    column_list = [c.name for c in Profile.__table__.columns]  # type: ignore
    form_columns = [c.name for c in Profile.__table__.columns]  # type: ignore


class ListingView(ModelView):
    column_list = [c.name for c in Listing.__table__.columns]  # type: ignore
    form_columns = [c.name for c in Listing.__table__.columns]  # type: ignore


class ListingImageView(ModelView):
    column_list = [c.name for c in ListingImage.__table__.columns]  # type: ignore
    form_columns = [c.name for c in ListingImage.__table__.columns]  # type: ignore


class WishlistItemView(ModelView):
    column_list = [c.name for c in WishlistItem.__table__.columns]  # type: ignore
    form_columns = [c.name for c in WishlistItem.__table__.columns]  # type: ignore


def init_admin(app):
    admin_panel.init_app(app)
    admin_panel.add_view(UserView(User, db.session))
    admin_panel.add_view(ProfileView(Profile, db.session))
    admin_panel.add_view(ListingView(Listing, db.session))
    admin_panel.add_view(ListingImageView(ListingImage, db.session))
    admin_panel.add_view(WishlistItemView(WishlistItem, db.session))
    return admin_panel
