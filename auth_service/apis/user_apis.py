"""
Apis to register or handle users.
"""

from datetime import datetime, UTC

from fastapi import APIRouter, Body, Security
from fastapi.responses import JSONResponse, Response

from errorhub.decorator import api_exception_handler

from auth_service.models.users import User, UserRequest, UpdateUserRequest
from auth_service.logic.factory import factory
from auth_service.utils.helper import generate_user_id, raise_exception_if_not_valid_user
from auth_service.middleware.auth_dependency import get_current_user

router = APIRouter()


@router.post(
    "/users",
    tags=["Users"],
    responses={},
)
@api_exception_handler
async def register_user(
    payload: UserRequest = Body(..., embed=True),
):
    """
    Api to create user
    """
    user_id = await generate_user_id()

    user = User(
        id=user_id,
        name=payload.name,
        email=payload.email,
        password_hash=payload.password,
        apps=[payload.app_name],
    )
    user_service = factory.get_user_service()
    user_created = await user_service.register_user(user)
    return JSONResponse(
        status_code=201,
        content={"message": "User registered successfully", **user_created.model_dump(exclude={"password_hash"})},
    )


@router.delete("/users/{user_id}", tags=["Users"], responses={})
@api_exception_handler
async def delete_user(user_id: str, token_data=Security(get_current_user)):
    """
    Api to delete a user by user_id
    """
    await raise_exception_if_not_valid_user(user_id, token_data)
    user_service = factory.get_user_service()
    await user_service.delete_user(user_id)
    return Response(status_code=204)


@router.get("/users/{user_id}", tags=["Users"], responses={})
@api_exception_handler
async def get_user(user_id: str, email: str | None = None, token_data=Security(get_current_user)):
    """
    Api to get user information either by user_id or email
    """
    await raise_exception_if_not_valid_user(user_id, token_data)
    user_service = factory.get_user_service()
    user = await user_service.get_user_info(user_id=user_id, user_email=email)
    return JSONResponse(status_code=200, content=user.model_dump(exclude={"password_hash"}))


@router.put("/users/{user_id}", tags=["Users"], responses={})
@api_exception_handler
async def update_user(
    user_id: str,
    token_data=Security(get_current_user),
    payload: UpdateUserRequest = Body(..., embed=True),
    email: str | None = None,
):
    """
    Api to update user or return proper exceptions for errors
    """
    await raise_exception_if_not_valid_user(user_id, token_data)
    user_service = factory.get_user_service()
    user = User(
        id=user_id,
        name=payload.name,
        email=payload.email if payload.email is not None else "",
        password_hash=payload.password if payload.password is not None else "",
        apps=payload.app_name if payload.app_name is not None else [],
        updated_at=datetime.now(UTC).isoformat(),
        created_at="",  # This will be ignored in update
    )
    new_user = await user_service.update_user_by_id(user_id=user_id, user=user)
    return JSONResponse(status_code=200, content=new_user.model_dump(exclude={"password_hash"}))
