from fasttwilio.db_manager import get_collection
from fasttwilio.repositories.notification_repository import NotificationMonogoRepository
from fasttwilio.repositories.student_repository import StudentMonogoRepository
from fasttwilio.services.notification_service import NotificationService
from fasttwilio.services.student_service import StudentService


async def get_student_service() -> StudentService:
    collection = await get_collection("student")
    repository = StudentMonogoRepository(collection)
    return StudentService(repository)


async def get_notification_service() -> NotificationService:
    collection = await get_collection("notification")
    repository = NotificationMonogoRepository(collection)
    return NotificationService(repository)
