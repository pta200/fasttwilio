import logging
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, Security, status

from fasttwilio.dependencies import get_student_service
from fasttwilio.models import (
    StudentCollection,
    StudentModel,
    StudentPage,
    StudentPayload,
    StudentSearch,
)
from fasttwilio.services.auth_service import TokenData, validate_token
from fasttwilio.services.student_service import StudentService

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
    token: Annotated[TokenData, Security(validate_token, scopes=["write"])],
) -> StudentModel:
    """add new student

    Args:
        student (StudentModel): student payload
        student_collection (Annotated[Collection, get_student_service]): student collection

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
    token: Annotated[TokenData, Security(validate_token, scopes=["read"])],
    offset: int = 0,
    limit: int = Query(default=1000, le=1000),
) -> StudentCollection:
    """get list of students

    Args:
        student_collection (Annotated[Collection, get_student_service]): student collection
        offset (int, optional): find  offset. Defaults to 0.
        limit (int, optional): find limit. Defaults to Query(default=1000, le=1000).

    Returns:
        StudentCollection: lost of students
    """
    return await service.list_all(offset, limit)


@student_router.get(
    "/paginate",
    response_description="paginate lists all students",
    response_model=StudentPage,
    response_model_by_alias=False,
    operation_id="paginate_students",
)
async def paginate_students(
    service: Annotated[StudentService, Depends(get_student_service)],
    token: Annotated[TokenData, Security(validate_token, scopes=["read"])],
    offset: int = 0,
    limit: int = Query(default=1000, le=1000),
) -> StudentPage:
    """get a paginated list of students

    Args:
        student_collection (Annotated[Collection, get_student_service]): student collection
        offset (int, optional): find  offset. Defaults to 0.
        limit (int, optional): find limit. Defaults to Query(default=1000, le=1000).

    Returns:
        StudentCollection: lost of students
    """
    return await service.paginate(offset, limit)


@student_router.get(
    "/student/{student_id}",
    response_description="Get a single student",
    response_model=StudentModel,
    response_model_by_alias=False,
    operation_id="get_student",
)
async def get_student(
    student_id: uuid.UUID,
    service: Annotated[StudentService, Depends(get_student_service)],
    token: Annotated[TokenData, Security(validate_token, scopes=["read"])],
) -> StudentModel:
    """Get student by id

    Args:
        student_id (uuid.UUID): student id
        student_collection (Annotated[Collection, get_student_service]): student collection

    Returns:
        StudentModel: student document
    """
    if student := await service.get_by_id(student_id):
        return student

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="student {student_id} not found"
    )


@student_router.get(
    "/search",
    response_description="Student(s) found",
    response_model=StudentPage,
    response_model_by_alias=False,
    operation_id="search_student",
)
async def search(
    filter: Annotated[StudentSearch, Query()],
    service: Annotated[StudentService, Depends(get_student_service)],
    token: Annotated[TokenData, Security(validate_token, scopes=["write"])],
) -> StudentPage:
    """Search for students

    Args:
        filter (Annotated[StudentPayload, Query): student search fields
        service (Annotated[StudentService, Depends): student serice
        token (Annotated[TokenData, Security, optional): jwt token. Defaults to ["write"])].

    Raises:
        HTTPException: no students found

    Returns:
        StudentCollection: list of students
    """
    logger.info(f"SEARCHING FOR {filter}")
    if students := await service.search(filter):
        return students

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"not students found",
    )


@student_router.put(
    "/{student_id}",
    response_description="Update a student",
    response_model=StudentModel,
    response_model_by_alias=False,
    operation_id="update_student",
)
async def update_student(
    student_id: uuid.UUID,
    student_data: StudentPayload,
    service: Annotated[StudentService, Depends(get_student_service)],
    token: Annotated[TokenData, Security(validate_token, scopes=["write"])],
) -> StudentModel:
    """_summary_

    Args:
        student_id (uuid.UUID): student id
        student_data (StudentPayload): student data for update
        student_collection (Annotated[Collection, get_student_service]): student collection

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        StudentModel: StudentModel
    """
    if result := await service.update(student_id, student_data):
        return result

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Student {student_id} not found"
    )


@student_router.delete(
    "/{student_id}",
    response_description="Delete student",
    operation_id="delete_student",
)
async def delete_student(
    student_id: uuid.UUID,
    service: Annotated[StudentService, Depends(get_student_service)],
    token: Annotated[TokenData, Security(validate_token, scopes=["write"])],
) -> Response:
    """delete student

    Args:
        student_id (uuid.UUID): student id
        student_collection (Annotated[Collection, get_student_service]): student collection

    Returns:
        Response: sucessful removal
    """
    if await service.delete(student_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Student {id} not found"
    )
