from flask import Blueprint, request, jsonify
from app.services.example import UserService


example_bp = Blueprint('example', __name__)

@example_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    email = data.get("email")
    if not email or "@" not in email:
        return {"error": "invalid email"}, 400
    try:
        user = UserService.register(email)
        return jsonify(user.serialize()), 201
    except ValueError as e:
        return jsonify({"error": "Conflict", "message": f"Email {email} already registered"}), 400
    
  
@example_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = UserService.get_user_by_id(user_id)
    if user is None:
        return {"error": "User not found"}, 404
    return jsonify(user.serialize()), 200
  