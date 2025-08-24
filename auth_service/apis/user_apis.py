from datetime import datetime, UTC
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse, Response
from errorhub.decorator import api_exception_handler
from models.users import User, UserRequest
import uuid
from logic.factory import factory

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
    user_id = str(uuid.uuid4())
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
async def delete_user(user_id: str):
    user_service = factory.get_user_service()
    await user_service.delete_user(user_id)
    return Response(status_code=204)


@router.get("/users/{user_id}", tags=["Users"], responses={})
@api_exception_handler
async def get_user(user_id: str, email: str | None = None):
    user_service = factory.get_user_service()
    user = await user_service.get_user_info(user_id=user_id, user_email=email)
    return JSONResponse(status_code=200, content=user.model_dump(exclude={"password_hash"}))


@router.put("/users/{user_id}", tags=["Users"], responses={})
@api_exception_handler
async def update_user(user_id: str, payload: UserRequest = Body(..., embed=True), email: str | None = None):
    user_service = factory.get_user_service()
    user = await user_service.get_user_info(user_id=user_id, user_email=email)
    user.name = payload.name
    user.email = payload.email
    user.password_hash = payload.password
    user.updated_at = datetime.now(UTC).isoformat()
    await user_service.update_user_by_id(user_id=user_id, user=user)
    return JSONResponse(status_code=200, content=user.model_dump(exclude={"password_hash"}))
