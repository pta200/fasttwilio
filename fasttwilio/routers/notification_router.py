import logging
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, Security, status

from fasttwilio.dependencies import get_notification_service
from fasttwilio.models import (
    NotificationModel,
    NotificationPage,
    NotificationSearch,
)
from fasttwilio.services.auth_service import TokenData, validate_token
from fasttwilio.services.notification_service import NotificationService

logger = logging.getLogger(__name__)

notification_router = APIRouter(
    prefix="/notifications", tags=["Notifications"], responses={404: {"description": "not found"}}
)


@notification_router.post(
    "",
    response_description="Add new Notification",
    response_model=NotificationModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    operation_id="add_notification",
)
async def add_Notification(
    notification: NotificationModel,
    service: Annotated[NotificationService, Depends(get_notification_service)],
    token: Annotated[TokenData, Security(validate_token, scopes=["write"])],
) -> NotificationModel:
    """add notificaiton

    Args:
        notification (NotificationModel): model
        service (Annotated[NotificationService, Depends): Notification serice
        token (Annotated[TokenData, Security, optional): jwt token. Defaults to ["write"])].

    Returns:
        NotificationModel: _description_
    """
    return await service.add(notification)



@notification_router.get(
    "/notification/{notification_id}",
    response_description="Get a single Notification",
    response_model=NotificationModel,
    response_model_by_alias=False,
    operation_id="get_notification",
)
async def get_Notification(
    notification_id: uuid.UUID,
    service: Annotated[NotificationService, Depends(get_notification_service)],
    token: Annotated[TokenData, Security(validate_token, scopes=["read"])],
) -> NotificationModel:
    """get notification

    Args:
        Notification_id (uuid.UUID): _description_
        service (Annotated[NotificationService, Depends): Notification serice
        token (Annotated[TokenData, Security, optional): jwt token. Defaults to ["write"])].

    Raises:
        HTTPException: _description_

    Returns:
        NotificationModel: _description_
    """
    if Notification := await service.get_by_id(notification_id):
        return Notification

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Notification {Notification_id} not found"
    )


@notification_router.get(
    "/search",
    response_description="Notification(s) found",
    response_model=NotificationPage,
    response_model_by_alias=False,
    operation_id="search_notification",
)
async def search(
    filter: Annotated[NotificationSearch, Query()],
    service: Annotated[NotificationService, Depends(get_notification_service)],
    token: Annotated[TokenData, Security(validate_token, scopes=["write"])],
) -> NotificationPage:
    """Search for Notifications

    Args:
        filter (Annotated[NotificationPayload, Query): notification search fields
        service (Annotated[NotificationService, Depends): Notification serice
        token (Annotated[TokenData, Security, optional): jwt token. Defaults to ["write"])].

    Raises:
        HTTPException: no Notifications found

    Returns:
        NotificationCollection: list of Notifications
    """
    logger.info(f"SEARCHING FOR {filter}")
    if Notifications := await service.search(filter):
        return Notifications

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"not Notifications found",
    )


@notification_router.get(
    "/paginate",
    response_description="paginate lists all Notifications",
    response_model=NotificationPage,
    response_model_by_alias=False,
    operation_id="paginate_notifications",
)
async def paginate_Notifications(
    service: Annotated[NotificationService, Depends(get_notification_service)],
    token: Annotated[TokenData, Security(validate_token, scopes=["read"])],
    offset: int = 0,
    limit: int = Query(default=1000, le=1000),
) -> NotificationPage:
    """get a paginated list of Notifications

    Args:
        Notification_collection (Annotated[Collection, get_notification_service]): Notification collection
        offset (int, optional): find  offset. Defaults to 0.
        limit (int, optional): find limit. Defaults to Query(default=1000, le=1000).

    Returns:
        NotificationCollection: lost of Notifications
    """
    return await service.paginate(offset, limit)
