import asyncio
from typing import List, Dict
import uuid
from asyncio import current_task
from datetime import timedelta
import pytest_asyncio
from fastapi.testclient import TestClient

from fasttwilio.main import app
from fasttwilio.dependencies import get_student_service
from fasttwilio.models import StudentCollection, StudentModel, StudentPayload
from fasttwilio.services.student_service import StudentService
from fasttwilio.repositories.generic_repository import AbstractRepository


class InMemoryStudentRepository(AbstractRepository):

    def __init__(self, student_collection: Dict):
        self.student_collection = student_collection

    async def get_by_id(self, id: str) -> StudentModel:
        return self.student_collection.get(id)
    
    async def add(self, student: StudentModel) -> StudentModel:
        id = str(uuid.uuid4())
        student.student_id = id
        self.student_collection[id] = student
        return student
    
    async def list_all(self, offset: int, limit: int) -> List[StudentModel]:
        return self.student_collection.values()
    
    async def update(self, id: str, student: StudentModel) -> StudentModel:
        """Update an existing entity"""
        self.student_collection[id] = student
        return student

    async def delete(self, id: str) -> bool:
        """Remove an entity by its identifier"""
        try:
            student = self.student_collection.pop(id)
            return bool(student) 
        except KeyError:
            return False

async def override_get_student_service() -> StudentService:
    return StudentService(InMemoryStudentRepository({}))


app.dependency_overrides[get_student_service] = override_get_student_service

@pytest_asyncio.fixture(scope="function")
async def client() -> TestClient:
    # init test client with app without entering lifespan context
    return TestClient(app)