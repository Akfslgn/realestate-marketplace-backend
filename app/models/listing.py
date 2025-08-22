from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import mapped_column, relationship

from app.extensions import db


class Listing(db.Model):
    __tablename__ = "listings"
    id = mapped_column(Integer, primary_key=True)
    owner_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    title = mapped_column(String(255), nullable=False)
    description = mapped_column(Text, nullable=True)
    property_type = mapped_column(
        Enum("house", "apartment", "condo", "land", name="property_type_enum"),
        nullable=False,
        default="house",
    )
    price = mapped_column(Numeric(12, 2), nullable=False)
    bedrooms = mapped_column(Integer, nullable=True)
    bathrooms = mapped_column(Float, nullable=True)
    area_sqft = mapped_column(Integer, nullable=True)
    status = mapped_column(
        Enum("active", "pending", "sold", "inactive", name="listing_status_enum"),
        nullable=False,
        default="active",
    )
    address = mapped_column(String(255), nullable=True)
    city = mapped_column(String(100), nullable=True)
    state = mapped_column(String(100), nullable=True)
    zip_code = mapped_column(String(100), nullable=True)
    latitude = mapped_column(Float, nullable=True)
    longitute = mapped_column(Float, nullable=True)
    created_at = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    #   relationships:
    #     - listing_image one-to-many ListingImage
    #     - wishlist_item one-to-one WishlistItem
    owner = relationship("User", back_populates="listings")
    images = relationship("ListingImage", back_populates="listing", cascade="all, delete-orphan")
    wishlist_items = relationship("WishlistItem", back_populates="listing")

    def serialize(self):
        return {
            "id": self.id,
            "address": self.address,
            "owner_id": self.owner_id,
            "title": self.title,
            "description": self.description,
            "property_type": self.property_type,
            "price": float(self.price) if self.price else None,
            "bedrooms": self.bedrooms,
            "bathrooms": self.bathrooms,
            "area_sqft": self.area_sqft,
            "latitude": self.latitude,
            "longitude": self.longitute,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "images": [img.serialize() for img in self.images],
        }
