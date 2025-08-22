from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String(255), unique=True, nullable=False, index=True)
    username = mapped_column(String(255), unique=True,
                             nullable=False, index=True)
    password = mapped_column(String(255), nullable=False)
    is_active = mapped_column(Boolean, default=True, nullable=False)
    is_admin = mapped_column(Boolean, default=False, nullable=False)
    created_at = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    #   relationships:
    profile = relationship("Profile", back_populates="user", uselist=False)
    listings = relationship("Listing", back_populates="owner")
    wishlist_items = relationship("WishlistItem", back_populates="user")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "is_active": self.is_active,
            "is_admin": self.is_admin,
            # "created_at": self.created_at,
            # "updated_at": self.updated_at,
            "profile_information": self.profile.serialize(),
            "owned_listings": [listing.serialize() for listing in self.listings],
            "wishlisted_items": [i.serialize() for i in self.wishlist_items],
        }
