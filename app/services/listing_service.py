from typing import Any, Dict, List, Optional

from app.models.listing import Listing
from app.models.listing_image import ListingImage
from app.repositories.listing_image_repository import ListingImageRepository
from app.repositories.listing_repository import ListingRepository


class ListingService:
    @staticmethod
    def create_listing(owner_id: int, title: str, price: float, data: Dict[str, Any]) -> Listing:
        extra_data = {
            key: value for key, value in data.items() if key not in ("owner_id", "title", "price")
        }
        return ListingRepository.create(
            owner_id=owner_id, title=title, price=price, additional_data=extra_data
        )

    @staticmethod
    def get_all_listings() -> List[Listing]:
        return ListingRepository.get_all()

    @staticmethod
    def get_listings_by_id(listing_id: int) -> Optional[Listing]:
        return ListingRepository.get_by_id(listing_id)

    @staticmethod
    def get_listings_by_owner_id(owner_id: int) -> List[Listing]:
        return ListingRepository.get_by_owner_id(owner_id)

    @staticmethod
    def update_listing_by_id(listing_id: int, **kwargs) -> Listing:
        listing = ListingRepository.get_by_id(listing_id)
        if not listing:
            raise ValueError(f"Listing with id {listing_id} not found.")

        for key, value in kwargs.items():
            if hasattr(listing, key):
                setattr(listing, key, value)

        return ListingRepository.update(listing)

    @staticmethod
    def delete_listing_by_id(listing_id: int) -> bool:
        listing = ListingRepository.get_by_id(listing_id)
        if not listing:
            raise ValueError(f"Listing with id {listing_id} not found.")
        return ListingRepository.delete(listing)

    @staticmethod
    def add_listing_image(
        listing_id: int, image_url: str, claudinary_public_id: str, is_primary: bool, caption: str
    ) -> Optional[ListingImage]:

        listing = ListingRepository.get_by_id(listing_id)
        if not listing:
            return None

        image = ListingImageRepository.create(
            listing_id=listing_id,
            image_url=image_url,
            claudinary_public_id=claudinary_public_id,
            is_primary=is_primary,
            caption=caption,
        )

        return image

    @staticmethod
    def delete_listing_image(image_id: int, owner_id: int) -> bool:
        image = ListingImageRepository.get_by_id(image_id)
        if not image:
            return False

        listing = ListingRepository.get_by_id(image.listing_id)

        if not listing or listing.owner_id != owner_id:
            return False

        if not image:
            return False
        return ListingImageRepository.delete(image)

    @staticmethod
    def get_listing_image_by_id(image_id: int) -> Optional[ListingImage]:
        return ListingImageRepository.get_by_id(image_id)
