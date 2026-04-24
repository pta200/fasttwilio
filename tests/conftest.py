import asyncio
import uuid
from datetime import timedelta
from typing import Dict, List

import pytest_asyncio
from fastapi.testclient import TestClient

from fasttwilio.dependencies import get_student_service
from fasttwilio.main import app
from fasttwilio.models import StudentCollection, StudentModel, StudentPayload
from fasttwilio.repositories.generic_repository import AbstractRepository
from fasttwilio.services.auth_service import create_access_token
from fasttwilio.services.student_service import StudentService


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
        return StudentCollection(students=self.student_collection.values())

    async def update(self, id: str, student: StudentPayload) -> StudentModel:
        """Update an existing entity"""
        orig_student = self.student_collection[id]
        tmp_student = {}
        for k, v in orig_student.model_dump(by_alias=False).items():
            if k == "student_id":
                tmp_student[k] = v
            elif v != getattr(student, k) and getattr(student, k) is not None:
                tmp_student[k] = getattr(student, k)
            else:
                tmp_student[k] = v

        new_student = StudentModel(**tmp_student)
        self.student_collection[id] = new_student
        return new_student

    async def delete(self, id: str) -> bool:
        """Remove an entity by its identifier"""
        try:
            student = self.student_collection.pop(id)
            return bool(student)
        except KeyError:
            return False


# init repos only once since overide will get called each API call
repo = InMemoryStudentRepository({})


async def override_get_student_service() -> StudentService:
    """Depencey override with in memory repos"""
    return StudentService(repo)


app.dependency_overrides[get_student_service] = override_get_student_service


@pytest_asyncio.fixture(scope="function")
async def client() -> TestClient:
    # init test client with app without entering lifespan context
    return TestClient(app)


@pytest_asyncio.fixture(scope="function")
async def token() -> str:
    access_token = await create_access_token(
        data={"sub": "tester", "scope": ["read", "write"]},
        expires_delta=timedelta(minutes=5),
    )
    return access_token
