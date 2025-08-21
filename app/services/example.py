from app.repositories.example import UserRepository
from app.models.example import User
from typing import Optional

class UserService:
    @staticmethod
    def register(email: str) -> User:
        if UserRepository.get_by_email(email):
            raise ValueError("email already taken")
        return UserRepository.create_user(email=email)
    
    @staticmethod
    def get_user_by_id(id: int) -> Optional[User]:
        return UserRepository.get_by_id(id)