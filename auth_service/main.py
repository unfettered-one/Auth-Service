"""
Entry point for the Auth-Service API.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from errorhub.exceptions import ErrorHubException
from apis.user_apis import router as user_router
from apis.auth_apis import router as auth_router

from mangum import Mangum

app = FastAPI(
    title="Auth-Service",
    description="API for Auth-Service",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(auth_router)

mangum_handler = Mangum(app)


# Global Exception Handler
@app.exception_handler(ErrorHubException)
async def errorhub_exception_handler(request: Request, exc: ErrorHubException):
    """
    Catch all ErrorHubExceptions and return structured JSON response.
    The FastAPI exception handler receives the request as the first
    positional argument and the exception as the second.
    """
    return JSONResponse(status_code=exc.error_detail.code, content=exc.to_dict())

