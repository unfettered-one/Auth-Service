"""
Entry point for the Auth-Service API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from errorhub.exceptions import ErrorHubException
from apis.user_apis import router as user_router

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


# Global Exception Handler
@app.exception_handler(ErrorHubException)
async def errorhub_exception_handler(exc: ErrorHubException):
    """
    Catch all ErrorHubExceptions and return structured JSON response.
    """
    return JSONResponse(status_code=exc.error_detail.code, content=exc.to_dict())
