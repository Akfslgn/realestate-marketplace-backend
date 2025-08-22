from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models.listing import Listing
from app.models.wishlist_item import WishlistItem


class WishlistItemRepository:
    @staticmethod
    def create(user_id: int, listing_id: int) -> WishlistItem:
        item = WishlistItem(user_id=user_id, listing_id=listing_id)  # type: ignore

        try:
            db.session().add(item)
            db.session().commit()
            return item
        except IntegrityError:
            db.session().rollback()
            raise ValueError("This listing is already added to the wishlist.")

    @staticmethod
    def get_by_user(user_id: int) -> List[WishlistItem]:
        stmt = select(WishlistItem).where(WishlistItem.user_id == user_id)
        results = db.session.execute(stmt)
        return list(results.scalars().all())

    @staticmethod
    def get_by_id(item_id: int) -> Optional[WishlistItem]:
        stmt = select(WishlistItem).where(WishlistItem.id == item_id)
        results = db.session.execute(stmt)
        return results.scalars().first()

    @staticmethod
    def get_listings_by_user(user_id: int) -> List[Listing]:
        stmt = select(Listing).join(WishlistItem, WishlistItem.user_id == user_id)
        results = db.session.execute(stmt)
        return list(results.scalars().all())

    @staticmethod
    def get_by_user_and_listing(user_id: int, listing_id: int) -> Optional[WishlistItem]:
        stmt = select(WishlistItem).where(
            WishlistItem.user_id == user_id, WishlistItem.listing_id == listing_id
        )
        result = db.session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    def delete(item: WishlistItem) -> bool:
        db.session.delete(item)
        db.session.commit()
        return True

    @staticmethod
    def delete_by_user_and_listing(user_id: int, listing_id: int) -> bool:
        item = WishlistItemRepository.get_by_user_and_listing(user_id, listing_id)
        if item:
            WishlistItemRepository.delete(item)
            return True
        return False
