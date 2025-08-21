from flask import jsonify
from app.extensions import db

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad request", "message": str(error)}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found", "message": str(error)}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": "Method Not Allowed", "message": str(error)}), 405
    
    @app.errorhandler(415)
    def unsuported_media_type(error):
        return jsonify({"error": "Unsupported Media Type", "message": str(error)}), 415

    @app.errorhandler(500)
    def internal_server_error(error):
        db.session.rollback()
        return jsonify({"error": "Internal server error", "message": str(error)}), 500
        
    @app.errorhandler(422)
    def handle_validation_error(error):
        return jsonify({"error": "Validation error", "message": error.description}), 422