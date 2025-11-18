import uuid
from datetime import datetime, UTC

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse, Response

from errorhub.decorator import api_exception_handler

from models.users import User, UserRequest
from logic.factory import factory

router = APIRouter()

