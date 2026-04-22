from fasttwilio.db_manager import get_student_collection
from fasttwilio.services.student_service import StudentService
from fasttwilio.repositories.student_repository import StudentMonogoRepository

async def get_student_service() -> StudentService:
    collection = await get_student_collection()
    repository = StudentMonogoRepository(collection)
    return StudentService(repository)
