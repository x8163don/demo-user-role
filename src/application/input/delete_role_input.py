from dataclasses import dataclass

from src.application.input.base import RegionInput, dedupe
from src.domain.aggregates.role import Role
from src.domain.entities.role.data_subject import DataSubject
from src.domain.entities.role.table import Table


@dataclass
class DeleteRoleInput(RegionInput):
    role_id: int

    def __post_init__(self):
        self.data_subject_ids = dedupe(self.data_subject_ids)
        self.table_ids = dedupe(self.table_ids)

    def to_domain(self) -> Role:
        result = Role(id=self.role_id)
        return result
