from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from app.extensions import db


class ListingImage(db.Model):
    __tablename__ = "listing_images"
    id = mapped_column(Integer, primary_key=True)
    listing_id = mapped_column(Integer, ForeignKey("listings.id"), nullable=False)
    image_url = mapped_column(String(255), nullable=True)
    claudinary_public_id = mapped_column(String(255), nullable=False)
    is_primary = mapped_column(Boolean, default=False, nullable=False)
    caption = mapped_column(String(255), nullable=True)
    created_at = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    #   relationships:
    listing = relationship("Listing", back_populates="images")

    def serialize(self):
        return {
            "id": self.id,
            "listing_id": self.listing_id,
            "image_url": self.image_url,
            "claudinary_public_id": self.claudinary_public_id,
            "is_primary": self.is_primary,
            "caption": self.caption,
            "created_at": self.created_at,
        }
