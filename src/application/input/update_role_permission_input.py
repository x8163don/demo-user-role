from dataclasses import dataclass

from src.application.input.base import RegionInput, dedupe
from src.domain.aggregates.role import Role
from src.domain.entities.role.data_subject import DataSubject
from src.domain.entities.role.table import Table


@dataclass
class UpdateRolePermissionInput(RegionInput):
    id: int
    name: str
    data_subject_ids: list[int]
    table_ids: list[int]

    def __post_init__(self):
        self.data_subject_ids = dedupe(self.data_subject_ids)
        self.table_ids = dedupe(self.table_ids)

    def to_domain(self) -> Role:
        result = Role(id=self.id, name=self.name)

        data_subjects = []
        for data_subject in self.data_subject_ids:
            data_subjects.append(DataSubject(id=data_subject))
        result.data_subjects = data_subjects

        tables = []
        for table_id in self.table_ids:
            tables.append(Table(id=table_id))
        result.tables = tables

        return result
