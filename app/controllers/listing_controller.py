import cloudinary.uploader
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.listing_service import ListingService

listing_bp = Blueprint("listings", __name__)


@listing_bp.route("/listings", methods=["POST"])
@jwt_required()
def create_listing():
    # capture the data from request
    data = request.get_json()

    if not data:
        return jsonify({"error": "400 Bad Request", "message": "Data as JSON not provided"}), 400

    # Add validation for property_type
    # Must match the enum values in the database model
    valid_property_types = ["house", "apartment", "condo", "land"]
    if "property_type" in data and data.get("property_type").lower() not in valid_property_types:
        return jsonify({
            "error": "400 Bad Request",
            "message": f"Invalid property_type. Must be one of: {', '.join(valid_property_types)}"
        }), 400

    # Convert property_type to lowercase to match enum
    if "property_type" in data:
        data["property_type"] = data["property_type"].lower()

    if "owner_id" not in data or not data.get("owner_id"):
        return (
            jsonify(
                {"error": "400 Bad Request",
                    "message": "Required field 'owner_id' is missing"}
            ),
            400,
        )

    user_id_jwt = int(get_jwt_identity())

    if not user_id_jwt == data.get("owner_id"):
        return jsonify({"error": "You are not authorized to access this account."})

    if "title" not in data or not data.get("title"):
        return (
            jsonify({"error": "400 Bad Request",
                    "message": "Required field 'title' is missing"}),
            400,
        )

    if "price" not in data or not data.get("price"):
        return (
            jsonify({"error": "400 Bad Request",
                    "message": "Required field 'price' is missing"}),
            400,
        )

    listing = ListingService.create_listing(
        owner_id=data.get("owner_id"), title=data.get("title"), price=data.get("price"), data=data
    )

    if listing:
        return (
            jsonify(
                {"message": "Successfully created a new listing",
                    "listing": listing.serialize()}
            ),
            201,
        )
    else:
        return jsonify({"message": "Something went wrond while creating the listing"}), 400


@listing_bp.route("/listings", methods=["GET"])
def get_all_listings():
    listings = ListingService.get_all_listings()
    if listings:
        return jsonify([listing.serialize() for listing in listings])
    else:
        return jsonify({"message": "Seems like there is an issue"}), 404


@listing_bp.route("/listings/<int:listing_id>", methods=["GET"])
def get_listing_by_id(listing_id: int):
    listing = ListingService.get_listings_by_id(listing_id)

    if listing:
        return jsonify(listing.serialize()), 200
    else:
        return jsonify({"error": f"Listing with id {listing_id} not found"}), 404


@listing_bp.route("/listings/owner/<int:owner_id>", methods=["GET"])
@jwt_required()
def get_listings_by_owner_id(owner_id: int):
    listings = ListingService.get_listings_by_owner_id(owner_id)
    if listings:
        return jsonify([listing.serialize() for listing in listings]), 200
    else:
        return jsonify({"error": f"Listings not found for given owner(user) id {owner_id}"}), 404


@listing_bp.route("/listings/<int:listing_id>", methods=["PUT"])
@jwt_required()
def update_listing(listing_id: int):
    # capture the data from request
    data = request.get_json()

    if not data:
        return jsonify({"error": "400 Bad Request", "message": "Data as JSON not provided"}), 400

    if "owner_id" in data:
        return (
            jsonify({"error": "400 Bad Request",
                    "message": "Not allowed to change the owner id."}),
            400,
        )

    user_id_jwt = int(get_jwt_identity())

    if not user_id_jwt == data.get("owner_id"):
        return jsonify({"error": "You are not authorized to access this account."})

    try:
        listing = ListingService.update_listing_by_id(
            listing_id=listing_id, **data)
        return (
            jsonify(
                {"message": "Successfully created a new listing",
                    "listing": listing.serialize()}
            ),
            200,
        )
    except ValueError as e:
        return jsonify({"message": str(e)}), 404


@listing_bp.route("/listings/<int:listing_id>", methods=["DELETE"])
@jwt_required()
def delete_listing(listing_id: int):
    listing = ListingService.get_listings_by_id(listing_id)

    if not listing:
        return jsonify({"error": f"No Listing Found With ID {listing_id}"})

    user_id_jwt = int(get_jwt_identity())

    if not user_id_jwt == listing.owner_id:
        return jsonify({"error": "You are not authorized to access this account."})

    try:
        success = ListingService.delete_listing_by_id(listing_id)
        if success:
            return jsonify({"message": f"Listing with id {listing_id} successfully deleted"})
        else:
            return jsonify({"error": f"Listing with id {listing_id} failed to be deleted"})
    except ValueError as e:
        return jsonify({"error": "No Found", "message": str(e)})


@listing_bp.route("/listings/<int:listing_id>/images", methods=["POST"])
@jwt_required()
def upload_image(listing_id: int):
    listing = ListingService.get_listings_by_id(listing_id)

    if not listing:
        return jsonify({"error": f"Listing with id {listing_id} Not Found"}), 404

    if not request.content_type.startswith("multipart/form-data"):
        return jsonify({"error": "Content type should be multipart/form-data"})

    if "image" not in request.files:
        return jsonify({"error": "Image not provided"}), 400

    image_file = request.files.get("image")
    is_primary = request.form.get("is_primary", "")
    caption = request.form.get("caption", "")

    # upload image to claudinary
    upload_result = cloudinary.uploader.upload(
        image_file, folder="listing_images")
    print("upload_result", upload_result)
    # create a new listing image object

    listing_image = ListingService.add_listing_image(
        listing_id=listing_id,
        image_url=upload_result.get("secure_url"),
        claudinary_public_id=upload_result.get("public_id"),
        is_primary=True if is_primary.lower() == "true" else False,
        caption=caption,
    )

    if listing_image:
        return jsonify(listing_image.serialize()), 201
    else:
        return jsonify({"error": "Could not upload the image due to not existing listing"}), 404


# TODO - Fix the issue with deleting the listing image that doesnt belog to that listing
@listing_bp.route("/listings/<int:listing_id>/images/<int:image_id>", methods=["DELETE"])
@jwt_required()
def delete_image(listing_id: int, image_id: int):
    listing = ListingService.get_listings_by_id(listing_id)

    if not listing:
        return jsonify({"message": f"No such listing id {listing_id}"}), 404

    image_to_delete = ListingService.get_listing_image_by_id(image_id)

    if not image_to_delete:
        return jsonify({"message": f"No such image id {image_id}"}), 404

    # delete image function
    result = ListingService.delete_listing_image(image_id, listing.owner_id)
    if not result:
        return jsonify({"error": "Access denied or image not found."})

    cloudinary.uploader.destroy(image_to_delete.claudinary_public_id)

    if result:
        return jsonify({"message": f"Image with id {image_id} successfully deleted."}), 200
    else:
        return jsonify({"error": "Something went wrong"}), 400
