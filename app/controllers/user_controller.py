import cloudinary.uploader
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.user_service import UserService
from app.utils.validators import is_valid_email, is_valid_password, is_valid_username

user_bp = Blueprint("users", __name__)


@user_bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_by_id(user_id: int):

    user_id_jwt = int(get_jwt_identity())

    if not user_id_jwt == user_id:
        return jsonify({"error": "You are not authorized to access this account."})

    # have accessed the service layer to get one user
    user = UserService.get_user_by_id(user_id)

    if user:
        return jsonify(user.serialize()), 200
    else:
        return (
            jsonify({"error": "404 Not Found", "message": f"User with id: {user_id} not found."}),
            404,
        )


@user_bp.route("/users/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user_by_id(user_id: int):

    user_id_jwt = int(get_jwt_identity())

    if not user_id_jwt == user_id:
        return jsonify({"error": "You are not authorized to access this account."})

    # need to get the user by id
    user = UserService.get_user_by_id(user_id)
    if not user:
        return (
            jsonify({"error": "404 Not Found", "message": f"User with id: {user_id} not found."}),
            404,
        )

    data = request.get_json()
    if not data:
        return jsonify({"error": "400 Bad Request", "message": "Data as JSON not provided"}), 400

    # Manual validation
    if "email" in data and (not data.get("email") or not is_valid_email(data.get("email"))):
        return jsonify({"error": "email property fails validation"}), 400

    if "username" in data and (
        not data.get("username") or not is_valid_username(data.get("username"))
    ):
        return jsonify({"error": "username property fails validation"}), 400

    if "password" in data and (
        not data.get("password") or not is_valid_password(data.get("password"))
    ):
        return jsonify({"error": "password property fails validation"}), 400

    # once validation passed we update the record
    updated_user = UserService.update_user(user, **data)

    if updated_user:
        return (
            jsonify({"message": "User Successfully updated", "user": updated_user.serialize()}),
            200,
        )
    else:
        return jsonify({"message": "Something went wrong while updating the user information"}), 400


@user_bp.route("/users/<int:user_id>/profile", methods=["GET"])
@jwt_required()
def get_user_profile(user_id: int):
    user_id_jwt = int(get_jwt_identity())

    if not user_id_jwt == user_id:
        return jsonify({"error": "You are not authorized to access this account."})

    # find the profile
    profile = UserService.get_profile_by_user_id(user_id)

    if profile:
        return jsonify(profile.serialize()), 200
    else:
        return (
            jsonify({"error": "404 Not Found", "message": f"User with id: {user_id} not found."}),
            404,
        )


@user_bp.route("/users/<int:user_id>/profile", methods=["PUT"])
@jwt_required()
def update_user_profile(user_id: int):
    user_id_jwt = int(get_jwt_identity())

    if not user_id_jwt == user_id:
        return jsonify({"error": "You are not authorized to access this account."})

    profile = UserService.get_profile_by_user_id(user_id)

    if not profile:
        return (
            jsonify({"error": "404 Not Found", "message": f"User with id: {user_id} not found."}),
            404,
        )

    data = request.get_json()

    if not data:
        return jsonify({"error": "400 Bad Request", "message": "Data as JSON not provided"}), 400

    # update data
    try:
        profile = UserService.update_user_profile(user_id, data)
        return jsonify(
            {"message": "User profile successfully updated.", "profile": profile.serialize()}
        )
    except ValueError as e:
        return jsonify({"error": "Something went wrond", "message": str(e)})


@user_bp.route("/users/<int:user_id>/profile/image", methods=["PATCH"])
@jwt_required()
def update_user_profile_image(user_id: int):
    user_id_jwt = int(get_jwt_identity())

    if not user_id_jwt == user_id:
        return jsonify({"error": "You are not authorized to access this account."})

    profile = UserService.get_profile_by_user_id(user_id)
    if not profile:
        return jsonify({"error": "User Not Found"}), 404

    if not request.content_type.startswith("multipart/form-data"):
        return jsonify({"error": "Content type should be multipart/form-data"})

    image_file = request.files.get("image")

    if not image_file:
        return jsonify({"error": "Image not provided"}), 400

    if profile.cloudinary_public_id:
        print(f"cloudinary public id {profile.cloudinary_public_id}")
        cloudinary.uploader.destroy(profile.cloudinary_public_id)

    uploaded_result = cloudinary.uploader.upload(image_file, folder="profile_images")
    print(uploaded_result)
    profile.avatar_url = uploaded_result["secure_url"]
    profile.cloudinary_public_id = uploaded_result["public_id"]

    UserService.update_user_profile(
        user_id,
        {"avatar_url": profile.avatar_url, "cloudinary_public_id": profile.cloudinary_public_id},
    )

    return jsonify({"message": "successfully uploaded image", "profile": profile.serialize()})
