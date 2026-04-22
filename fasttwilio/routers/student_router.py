import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status, Response
from pymongo import ReturnDocument
from pymongo.asynchronous.collection import AsyncCollection

from fasttwilio.services.student_service import StudentService
from fasttwilio.dependencies import get_student_service
from fasttwilio.db_manager import get_student_collection
from fasttwilio.models import ObjectId, StudentCollection, StudentModel, StudentPayload

logger = logging.getLogger(__name__)

student_router = APIRouter(
    prefix="/students", tags=["students"], responses={404: {"description": "not found"}}
)

@student_router.post(
    "",
    response_description="Add new student",
    response_model=StudentModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    operation_id="add_student",
)
async def add_student(
    student: StudentModel,
    service: Annotated[StudentService, Depends(get_student_service)],
) -> StudentModel:
    """add new student

    Args:
        student (StudentModel): student payload
        student_collection (Annotated[Collection, get_student_collection]): student collection

    Returns:
        StudentModel: resulting student document
    """
    return await service.add(student)


@student_router.get(
    "",
    response_description="list all students",
    response_model=StudentCollection,
    response_model_by_alias=False,
    operation_id="get_students",
)
async def list_students(
    service: Annotated[StudentService, Depends(get_student_service)],
    offset: int = 0,
    limit: int = Query(default=1000, le=1000),
) -> StudentCollection:
    """get a paginated list of students

    Args:
        student_collection (Annotated[Collection, get_student_collection]): student collection
        offset (int, optional): find  offset. Defaults to 0.
        limit (int, optional): find limit. Defaults to Query(default=1000, le=1000).

    Returns:
        StudentCollection: lost of students
    """
    return await service.list_all(offset, limit)


@student_router.get(
    "/{student_id}",
    response_description="Get a single student",
    response_model=StudentModel,
    response_model_by_alias=False,
    operation_id="get_student",
)
async def get_student(
    student_id: str,
    service: Annotated[StudentService, Depends(get_student_service)],
) -> StudentModel:
    """Get student by id

    Args:
        student_id (str): student id
        student_collection (Annotated[Collection, get_student_collection]): student collection

    Returns:
        StudentModel: student document
    """
    if (student := await service.get_by_id(student_id)):
        return student

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="student {student_id} not found")

@student_router.get(
    "/search/{student_name}",
    response_description="Get a single student",
    response_model=StudentModel,
    response_model_by_alias=False,
    operation_id="find_student_by_name"
)
async def find_by_name(
    student_name: str,
    service: Annotated[StudentService, Depends(get_student_service)],
) -> StudentModel:
    """Find student by name

    Args:
        student_name (str): student name
        student_collection (Annotated[AsyncCollection, Depends): student collection

    Raises:
        HTTPException: failed to find student

    Returns:
        StudentModel: student document
    """
    if student := await service.find_by_name(student_name):
        return student
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"student {student_name} not found")

@student_router.put(
    "/{student_id}",
    response_description="Update a student",
    response_model=StudentModel,
    response_model_by_alias=False,
    operation_id="update_student"
)
async def update_student(
    student_id: str,
    student_data: StudentPayload,
    service: Annotated[StudentService, Depends(get_student_service)],
) -> StudentModel:
    """_summary_

    Args:
        student_id (str): student id
        student_data (StudentPayload): student data for update
        student_collection (Annotated[Collection, get_student_collection]): student collection

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        StudentModel: StudentModel
    """
    if (result := await service.update(student_id, student_data)):
        return result
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student {student_id} not found")

@student_router.delete("{student_id", response_description="Delete student", operation_id="delete_student")
async def delete_student(student_id:str, service: Annotated[StudentService, Depends(get_student_service)],) -> Response:
    """delete student

    Args:
        student_id (str): student id
        student_collection (Annotated[Collection, get_student_collection]): student collection

    Returns:
        Response: sucessful removal
    """
    if await service.delete(student_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student {id} not found")


