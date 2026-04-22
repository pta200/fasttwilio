from pymongo import ReturnDocument
from pymongo.asynchronous.collection import AsyncCollection

from fasttwilio.repositories.generic_repository import AbstractRepository
from fasttwilio.models import StudentCollection, StudentModel, ObjectId, StudentPayload

class StudentMonogoRepository(AbstractRepository):

    def __init__(self, student_collection: AsyncCollection):
        self.student_collection = student_collection

    async def get_by_id(self, id: str) -> StudentModel:
        if student := await self.student_collection.find_one({"_id": ObjectId(id)}):
            return student
        return None
    
    async def add(self, student: StudentModel) -> StudentModel:
        new_student = student.model_dump(by_alias=True, exclude=["student_id"])
        result = await self.student_collection.insert_one(new_student)
        new_student["_id"] = result.inserted_id
        return new_student
        

    async def list_all(self, offset: int, limit: int) -> StudentCollection:
        return StudentCollection(
            students=await self.student_collection.find().skip(offset).limit(limit).to_list(limit)
        )
    
    async def update(self, id: str, student_data: StudentPayload) -> StudentModel:
        """Update an existing entity"""
        student = {
            k: v for k,v in student_data.model_dump(by_alias=True).items() if v is not None
        }

        if len(student) >= 1:
            result = await self.student_collection.find_one_and_update(
                {"_id": ObjectId(id)},
                {"$set": student},
                return_document=ReturnDocument.AFTER,
            )

            if result:
                return result
            raise ValueError(f"Student {id} not found")
        
        # The update is empty, so return the matching document:
        if (existing_student := await self.student_collection.find_one({"_id": ObjectId(id)})) is not None:
            return existing_student

    async def delete(self, id: str) -> bool:
        """Remove an entity by its identifier"""
        result = await self.student_collection.delete_one({"_id": ObjectId(id)})

        if result.deleted_count != 1:
            return False
        
        return True
        
    async def find_by_name(self, name: str) -> StudentModel:
        if student := await self.student_collection.find_one({"name": name}):
            return student
        return None
    