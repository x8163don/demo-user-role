from abc import ABC, abstractmethod

from result import Result

from src.domain.aggregates.role import Role


class RoleRepository(ABC):

    @abstractmethod
    def create(self, role: Role) -> Result[Role, str]:
        pass

    @abstractmethod
    def update(self, role: Role) -> Result[Role, str]:
        pass

    @abstractmethod
    def delete(self, role: Role) -> Result[Role, str]:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Result[Role, str]:
        pass
