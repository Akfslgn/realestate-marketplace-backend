from datetime import datetime, timezone
from sqlalchemy import String, DateTime, Integer
from sqlalchemy.orm import mapped_column
from app.extensions import db

class User(db.Model):
    __tablename__ = "example_users"
    id = mapped_column(
        Integer,
        primary_key=True)
    email = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True)
    created_at = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "created_at": self.created_at
        }
