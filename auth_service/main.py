from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Auth-Service",
    description="API for Auth-Service",
    version="0.0.1",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
