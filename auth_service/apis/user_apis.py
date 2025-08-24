from datetime import datetime, UTC
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from errorhub.decorator import api_exception_handler
from models.users import User, UserRequest
import uuid
from logic.factory import Factory

router = APIRouter()


@router.post(
    "/register",
    tags=["Users"],
    responses={},
)
@api_exception_handler
async def register_user(
    payload: UserRequest = Body(..., embed=True),
):
    user_id = uuid.uuid4()
    user_created_at_time = datetime.now(UTC)
    user_updated_at_time = datetime.now(UTC)
    user = User(
        id=user_id,
        name=payload.name,
        email=payload.email,
        created_at=user_created_at_time,
        updated_at=user_updated_at_time,
        password_hash=payload.password,
        apps=[payload.app_name],
    )
    user_service = Factory.get_user_service()
    await user_service.register_user(user)
    return JSONResponse(status_code=201, content={"message": "User registered successfully"})
