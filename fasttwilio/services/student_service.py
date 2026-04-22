import logging

from fasttwilio.repositories.student_repository import AbstractRepository
from fasttwilio.models import StudentCollection, StudentModel, StudentPayload

logger = logging.getLogger(__name__)

class StudentService:
    def __init__(self, repository: AbstractRepository):
        self.repository = repository
        logger.info("just added repos")

    async def get_by_id(self, id: str) -> StudentModel:
        return await self.repository.get_by_id(id)
    
    async def add(self, student: StudentModel) -> StudentModel:
        return await self.repository.add(student)
    
    async def list_all(self, offset: int, limit: int) -> StudentCollection:
        return await self.repository.list_all(offset, limit)
    
    async def update(self, id: str, student_data: StudentPayload) -> StudentModel:
        return await self.repository.update(id, student_data)

    async def delete(self, id: str) -> bool:
        return await self.repository.delete(id)
    
    async def find_by_name(self, name: str) -> StudentModel:
        return await self.repository.find_by_name(name)