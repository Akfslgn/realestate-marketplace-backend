from typing import List, Optional

from sqlalchemy import desc, select

from app.extensions import db
from app.models.listing import Listing


class ListingRepository:
    @staticmethod
    def create(owner_id: int, title: str, price: float, additional_data) -> Listing:
        listing = Listing(owner_id=owner_id, title=title, price=price)
        print("REPOSITORY LOG: ", listing.serialize())
        # set all additional attributes
        for key, value in additional_data.items():
            if hasattr(listing, key):
                setattr(listing, key, value)
        db.session.add(listing)
        db.session.commit()
        return listing

    @staticmethod
    def get_by_id(listing_id: int) -> Optional[Listing]:
        stmt = select(Listing).where(Listing.id == listing_id)
        result = db.session.execute(stmt)
        return result.scalars().first()

    @staticmethod
    def get_by_owner_id(owner_id: int) -> List[Listing]:
        stmt = select(Listing).where(Listing.owner_id == owner_id)
        results = db.session.execute(stmt)
        return list(results.scalars().all())

    @staticmethod
    def get_all(limit: int = 20, offset: int = 0) -> List[Listing]:
        stmt = select(Listing).order_by(desc(Listing.updated_at)).limit(limit).offset(offset)
        results = db.session.execute(stmt)
        return list(results.scalars().all())

    @staticmethod
    def update(listing: Listing) -> Listing:
        db.session.commit()
        return listing

    @staticmethod
    def delete(listing: Listing) -> bool:
        db.session.delete(listing)
        db.session.commit()
        return True
