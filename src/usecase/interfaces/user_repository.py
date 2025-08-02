from abc import ABC, abstractmethod

from result import Result

from domain.aggregates.user import User


class UserRepository(ABC):

    @abstractmethod
    def create(self, user: User) -> Result[User, str]:
        pass

    @abstractmethod
    def update(self, user: User) -> Result[User, str]:
        pass

    @abstractmethod
    def delete(self, user: User) -> Result[User, str]:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Result[User, str]:
        pass
