from fasttwilio.db_manager import get_student_collection
from fasttwilio.repositories.student_repository import StudentMonogoRepository
from fasttwilio.services.student_service import StudentService


async def get_student_service() -> StudentService:
    collection = await get_student_collection()
    repository = StudentMonogoRepository(collection)
    return StudentService(repository)
