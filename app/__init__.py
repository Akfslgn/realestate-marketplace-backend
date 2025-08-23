import cloudinary
from flask import Flask

from app.admin import init_admin
from app.config import get_config
from app.controllers.auth_controller import auth_bp
from app.controllers.listing_controller import listing_bp
from app.controllers.user_controller import user_bp
from app.controllers.wishlist_item_controller import wishlist_items_bp
from app.controllers.ai_controller import ai_bp
from app.error_handlers import register_error_handlers
from app.extensions import cors, db, jwt, migrate


def create_app(env: str | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config(env))

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, origins=app.config.get("CORS_ORIGINS", ["*"]))
    init_admin(app)
    jwt.init_app(app)

    cloudinary.config(
        cloud_name=app.config["CLOUDINARY_CLOUD_NAME"],
        api_key=app.config["CLOUDINARY_API_KEY"],
        api_secret=app.config["CLOUDINARY_API_SECRET"],
    )

    # Register error handlers
    register_error_handlers(app)

    # register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(user_bp, url_prefix="/api/v1")
    app.register_blueprint(listing_bp, url_prefix="/api/v1")
    app.register_blueprint(wishlist_items_bp, url_prefix="/api/v1")
    app.register_blueprint(ai_bp, url_prefix="/api/v1")

    # health check
    @app.get("/ping")
    def ping():
        return {"status": "ok"}

    return app
