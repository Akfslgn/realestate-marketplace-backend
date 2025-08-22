from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import mapped_column, relationship

from app.extensions import db


class WishlistItem(db.Model):
    __tablename__ = "wishlist_items"
    __table_args__ = (UniqueConstraint("user_id", "listing_id", name="uix_user_listing"),)
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    listing_id = mapped_column(Integer, ForeignKey("listings.id"), nullable=False)
    created_at = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    #   relationships:
    listing = relationship("Listing", back_populates="wishlist_items")
    user = relationship("User", back_populates="wishlist_items")

    def serialize(self):
        return {
            "id": self.id,
            "listing_id": self.listing_id,
            "user_id": self.user_id,
            "created_at": self.created_at,
        }
