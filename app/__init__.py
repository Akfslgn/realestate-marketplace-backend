import cloudinary
from flask import Flask, request

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

    # Initialize CORS with proper configuration
    cors.init_app(app,
                  origins=app.config.get("CORS_ORIGINS", ["*"]),
                  methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
                  allow_headers=["Content-Type", "Authorization"],
                  supports_credentials=True)

    init_admin(app)
    jwt.init_app(app)

    cloudinary.config(
        cloud_name=app.config["CLOUDINARY_CLOUD_NAME"],
        api_key=app.config["CLOUDINARY_API_KEY"],
        api_secret=app.config["CLOUDINARY_API_SECRET"],
    )

    # Register error handlers
    register_error_handlers(app)

    # Manual CORS headers as backup
    @app.after_request
    def after_request(response):
        origin = request.headers.get('Origin')
        if origin in app.config.get("CORS_ORIGINS", []):
            response.headers.add('Access-Control-Allow-Origin', origin)
            response.headers.add(
                'Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods',
                                 'GET,PUT,POST,DELETE,OPTIONS,PATCH')
            response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

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

    # database health check
    @app.get("/health")
    def health():
        try:
            # Simple database query to check connection
            db.session.execute(db.text("SELECT 1"))
            return {"status": "ok", "database": "connected"}
        except Exception as e:
            return {"status": "error", "database": "disconnected", "error": str(e)}, 500

    # seed endpoint for initial data
    @app.get("/seed")
    def seed():
        try:
            from app.models import User, Listing
            
            # Check if data already exists
            existing_users = db.session.query(User).count()
            if existing_users > 0:
                return {"message": "Database already seeded", "users": existing_users}
            
            # Create sample users
            sample_users = [
                User(email="admin@homehaven.com", username="admin"),
                User(email="user1@homehaven.com", username="user1"),
                User(email="user2@homehaven.com", username="user2")
            ]
            
            for user in sample_users:
                db.session.add(user)
            
            db.session.commit()
            return {"message": "Database seeded successfully", "users_created": len(sample_users)}
        except Exception as e:
            return {"error": str(e)}, 500

    return app
