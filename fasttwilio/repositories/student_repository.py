import logging
import uuid

import uuid_utils
from pymongo import ASCENDING, DESCENDING, ReturnDocument
from pymongo.asynchronous.collection import AsyncCollection

from fasttwilio.models import (
    Page,
    SortType,
    StudentCollection,
    StudentModel,
    StudentPayload,
)
from fasttwilio.repositories.generic_repository import AbstractRepository

logger = logging.getLogger(__name__)


class StudentMonogoRepository(AbstractRepository):

    def __init__(self, student_collection: AsyncCollection):
        self.student_collection = student_collection

    async def get_by_id(self, id: uuid.UUID) -> StudentModel:
        """Get student by id

        Args:
            id (uuid.UUID): id

        Returns:
            StudentModel: student
        """
        if student := await self.student_collection.find_one({"_id": id}):
            return student
        return None

    async def add(self, student: StudentModel) -> StudentModel:
        """Add a student

        Args:
            student (StudentModel): student data

        Raises:
            Exception: failed to add

        Returns:
            StudentModel: student response with id
        """
        new_student = student.model_dump(by_alias=True, exclude=["student_id"])
        new_student["_id"] = uuid.UUID(str(uuid_utils.uuid7()))
        result = await self.student_collection.insert_one(new_student)
        if result.inserted_id:
            return new_student

        raise Exception("failed to add student")

    async def list_all(self, offset: int, limit: int) -> StudentCollection:
        return StudentCollection(
            students=await self.student_collection.find()
            .skip(offset)
            .limit(limit)
            .to_list(limit)
        )

    async def update(self, id: uuid.UUID, student_data: StudentPayload) -> StudentModel:
        """Update an existing entity"""
        student = {
            k: v
            for k, v in student_data.model_dump(by_alias=True).items()
            if v is not None
        }

        if len(student) >= 1:
            result = await self.student_collection.find_one_and_update(
                {"_id": id},
                {"$set": student},
                return_document=ReturnDocument.AFTER,
            )

            if result:
                return result
            raise ValueError(f"Student {id} not found")

        # The update is empty, so return the matching document:
        if (
            existing_student := await self.student_collection.find_one({"_id": id})
        ) is not None:
            return existing_student

    async def delete(self, id: uuid.UUID) -> bool:
        """Remove an entity by its identifier"""
        result = await self.student_collection.delete_one({"_id": id})

        if result.deleted_count != 1:
            return False

        return True

    async def paginate(
        self, condition: dict, offset: int, limit: int, sort: dict[str, SortType]
    ) -> Page:
        """Paginate list of users

        Args:
            condition (dict): student attribute filter
            offset (int): start
            limit (int): end

        Returns:
            Page: List of students for UX page
        """
        if sort:
            logger.info("SORT BY")
            filter = []
            for k, v in sort.items():
                if v == "asc":
                    filter.append((k, ASCENDING))
                else:
                    filter.append((k, DESCENDING))
                return Page(
                    items=await self.student_collection.find(condition)
                    .sort(filter)
                    .skip(offset)
                    .limit(limit)
                    .to_list(limit),
                    total_items=await self.student_collection.count_documents(
                        condition
                    ),
                )

        else:
            return Page(
                items=await self.student_collection.find(condition)
                .skip(offset)
                .limit(limit)
                .to_list(limit),
                total_items=await self.student_collection.count_documents(condition),
            )
