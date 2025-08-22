from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from app.services.wishlist_items_service import WhishlistItemService

wishlist_items_bp = Blueprint("wishlist_items", __name__)


@wishlist_items_bp.route("/wishlist/<int:user_id>/listing/<int:listing_id>", methods=["POST"])
@jwt_required()
def add_wishlist_item(user_id: int, listing_id: int):
    try:
        item = WhishlistItemService.add_to_wishlist(user_id=user_id, listing_id=listing_id)
        return jsonify(item.serialize())
    except ValueError as e:
        return jsonify({"error": str(e)})


@wishlist_items_bp.route(
    "/wishlist/<int:user_id>/wishlist-item/<int:wishlist_item_id>", methods=["DELETE"]
)
@jwt_required()
def delete_wishlist_item(user_id: int, wishlist_item_id: int):
    item = WhishlistItemService.get_item_by_id(wishlist_item_id)
    if not item:
        return jsonify({"error": f"No such item with id {wishlist_item_id}"})

    result = WhishlistItemService.remove_item_from_wishlist(user_id, item.listing_id)
    if result:
        return jsonify({"message": "Item successfully deleted from wishlist"}), 200
    else:
        return jsonify({"error": "Item failed to deleted from wishlist"}), 400
