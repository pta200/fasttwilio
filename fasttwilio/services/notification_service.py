import logging
import uuid

from fasttwilio.models import NotificationModel, NotificationSearch, Page
from fasttwilio.repositories.generic_repository import AbstractRepository

logger = logging.getLogger(__name__)


class NotificationService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository
        logger.info("just added repos")

    async def get_by_id(self, id: uuid.UUID) -> NotificationModel:
        return await self.repository.get_by_id(id)

    async def add(self, student: NotificationModel) -> NotificationModel:
        return await self.repository.add(student)

    async def paginate(self, offset: int, limit: int) -> Page:
        return await self.repository.paginate({}, offset, limit)

    async def search(self, filter: NotificationSearch) -> Page:
        conditions = {}
        for k, v in filter.model_dump(exclude_none=True).items():
            if k in ("name", "email", "course"):
                conditions[k] = {"$regex": f"^{v}", "$options": "i"}
            elif k in ("offset", "limit"):
                continue
            else:
                conditions[k] = v

        return await self.repository.paginate(conditions, filter.offset, filter.limit)
