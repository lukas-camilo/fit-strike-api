from typing import Tuple, List, Optional

from src.application.repository.user_repository import UserRepository
from src.domain.entities.user import User


class GetUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, limit: int, last_evaluated_key=None) -> Tuple[List[User], Optional[dict]]:
        self.user_repository.get_users(limit=limit, last_evaluated_key=last_evaluated_key)