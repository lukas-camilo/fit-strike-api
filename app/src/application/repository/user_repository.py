from abc import ABC, abstractmethod
from typing import Tuple, List, Optional

from src.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def add_user(self, user: User) -> None:
        pass

    @abstractmethod
    def get_users(self, limit: int, last_evaluated_key=None) -> Tuple[List[User], Optional[dict]]:
        pass