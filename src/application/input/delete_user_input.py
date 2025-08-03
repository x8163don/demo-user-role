from dataclasses import dataclass

from src.application.input.base import RegionInput
from src.domain.aggregates.user import User


@dataclass
class DeleteUserInput(RegionInput):
    user_id: int

    def to_domain(self) -> User:
        result = User(id=self.user_id)
        return result
