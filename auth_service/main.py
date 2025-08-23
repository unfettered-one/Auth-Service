from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from errorhub.exceptions import ErrorHubException

from fastapi.responses import JSONResponse

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


# Global Exception Handler
@app.exception_handler(ErrorHubException)
async def errorhub_exception_handler(exc: ErrorHubException):
    """
    Catch all ErrorHubExceptions and return structured JSON response.
    """
    return JSONResponse(status_code=exc.error_detail.code, content=exc.to_dict())
