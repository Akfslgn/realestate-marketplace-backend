from typing import Any, Dict, Optional

from app.models.profile import Profile
from app.models.user import User
from app.repositories.profile_repository import ProfileRepository
from app.repositories.user_repository import UserRepository


class UserService:
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        return UserRepository.get_by_id(user_id)

    @staticmethod
    def update_user(user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            if hasattr(user, key):
                if key == "password":
                    user.set_password(value)
                else:
                    setattr(user, key, value)

        return UserRepository.update(user)

    @staticmethod
    def get_profile_by_user_id(user_id: int) -> Optional[Profile]:
        return ProfileRepository.get_by_user_id(user_id)

    @staticmethod
    def update_user_profile(user_id: int, data: Dict[str, Any]) -> Profile:
        profile = ProfileRepository.get_by_user_id(user_id)

        if not profile:
            raise ValueError(f"Profile with user_id {user_id} not found.")

        for key, value in data.items():
            if hasattr(profile, key):
                setattr(profile, key, value)

        return ProfileRepository.update(profile)

    @staticmethod
    def get_user_by_email(user_email: str) -> Optional[User]:
        return UserRepository.get_by_email(user_email)
