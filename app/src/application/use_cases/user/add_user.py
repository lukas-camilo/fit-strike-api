from src.application.repository.user_repository import UserRepository
from src.domain.entities.user import User


class AddUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, user_id: str, name: str, email: str) -> None:
        user = User(user_id=user_id, name=name, email=email)
        self.user_repository.add_user(user)