from dataclasses import dataclass
from typing import List

from src.application.input.base import dedupe, RegionInput
from src.domain.aggregates.user import User
from src.domain.entities.user.role import Role


@dataclass
class CreateUserInput(RegionInput):
    account: str
    role_ids: list[int]

    def __post_init__(self):
        self.role_ids = dedupe(self.role_ids)

    def to_domain(self) -> User:
        result = User(account=self.account)

        roles = list()
        for role_id in self.role_ids:
            roles.append(Role(id=role_id))

        result.roles = roles
        return result
