import logging
import uuid

from fasttwilio.models import (
    Page,
    Paginate,
    StudentCollection,
    StudentModel,
    StudentPayload,
    StudentSearch,
)
from fasttwilio.repositories.student_repository import AbstractRepository

logger = logging.getLogger(__name__)


class StudentService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository
        logger.info("just added repos")

    async def get_by_id(self, id: uuid.UUID) -> StudentModel:
        return await self.repository.get_by_id(id)

    async def add(self, student: StudentModel) -> StudentModel:
        return await self.repository.add(student)

    async def list_all(self, offset: int, limit: int) -> StudentCollection:
        return await self.repository.list_all(offset, limit)

    async def update(self, id: uuid.UUID, student_data: StudentPayload) -> StudentModel:
        return await self.repository.update(id, student_data)

    async def delete(self, id: uuid.UUID) -> bool:
        return await self.repository.delete(id)

    async def find_by_name(self, name: str) -> StudentCollection:
        return await self.repository.find_by_name(name)

    async def paginate(self, filter: Paginate) -> Page:
        sort = {}
        for k, v in filter.model_dump(exclude_none=True).items():
            if k in ("offset", "limit"):
                continue
            else:
                sort[k] = v
        return await self.repository.paginate({}, filter.offset, filter.limit, sort)

    async def search(self, filter: StudentSearch) -> Page:
        conditions = {}
        for k, v in filter.model_dump(exclude_none=True).items():
            if k in ("name", "email", "course"):
                conditions[k] = {"$regex": f"^{v}", "$options": "i"}
            elif k in ("offset", "limit"):
                continue
            else:
                conditions[k] = v

        return await self.repository.paginate(
            conditions, filter.offset, filter.limit, None
        )
