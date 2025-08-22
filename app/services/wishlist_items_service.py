from typing import Optional

from app.models.wishlist_item import WishlistItem
from app.repositories.listing_repository import ListingRepository
from app.repositories.user_repository import UserRepository
from app.repositories.wishlist_item_repository import WishlistItemRepository


class WhishlistItemService:
    @staticmethod
    def add_to_wishlist(user_id: int, listing_id: int) -> WishlistItem:
        listing = ListingRepository.get_by_id(listing_id)
        if not listing:
            raise ValueError(f"Listing with id {listing_id} not found")
        return WishlistItemRepository.create(user_id=user_id, listing_id=listing_id)

    @staticmethod
    def remove_item_from_wishlist(user_id: int, listing_id: int) -> bool:
        return WishlistItemRepository.delete_by_user_and_listing(user_id, listing_id)

    @staticmethod
    def get_wishlist_items_by_user_id(user_id: int):
        user = UserRepository.get_by_id(user_id)
        if not user:
            return None
        return WishlistItemRepository.get_by_user(user_id)

    @staticmethod
    def get_item_by_id(item_id: int) -> Optional[WishlistItem]:
        return WishlistItemRepository.get_by_id(item_id)
