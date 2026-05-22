import logging
import uuid

import uuid_utils
from pymongo import ReturnDocument
from pymongo.asynchronous.collection import AsyncCollection

from fasttwilio.models import (
    NotificationModel,
    NotificationPage
)
from fasttwilio.repositories.generic_repository import AbstractRepository

logger = logging.getLogger(__name__)


class NotificationMonogoRepository(AbstractRepository):

    def __init__(self, notification_collection: AsyncCollection):
        self.notification_collection = notification_collection

    async def get_by_id(self, id: uuid.UUID) -> NotificationModel:
        """Get notification by id

        Args:
            id (uuid.UUID): id

        Returns:
            NotificationModel: notification
        """
        if student := await self.notification_collection.find_one({"_id": id}):
            return student
        return None

    async def add(self, notification: NotificationModel) -> NotificationModel:
        """Add a student

        Args:
            student (NotificationModel): student data

        Raises:
            Exception: failed to add

        Returns:
            NotificationModel: student response with id
        """
        new_notification = notification.model_dump(by_alias=True, exclude=["student_id"])
        new_notification["_id"] = uuid.UUID(str(uuid_utils.uuid7()))
        result = await self.notification_collection.insert_one(new_notification)
        if result.inserted_id:
            return new_notification
        

    async def list_all(self, offset: int, limit: int) -> NotificationPage:
        """Paginate over entities"""
        raise NotImplementedError
    
    async def update(self, id: uuid.UUID, notification: NotificationModel) -> NotificationModel:
        """Update an existing entity"""
        raise NotImplementedError
        

    async def delete(self, id: uuid.UUID) -> bool:
        """Remove an entity by its identifier"""
        result = await self.notification_collection.delete_one({"_id": id})

        if result.deleted_count != 1:
            return False

        return True

    async def paginate(self, condition: dict, offset: int, limit: int) -> NotificationPage:
        """Paginate list of users

        Args:
            condition (dict): student attribute filter
            offset (int): start
            limit (int): end

        Returns:
            NotificationPage: List of students for UX page
        """
        return NotificationPage(
            items=await self.notification_collection.find(condition)
            .skip(offset)
            .limit(limit)
            .to_list(limit),
            total_items=await self.notification_collection.count_documents(condition),
        )

