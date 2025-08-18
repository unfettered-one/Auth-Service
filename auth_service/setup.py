from setuptools import setup, find_packages

setup(
    name="auth_service",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.116.1",
        "uvicorn==0.35.0",
        "pydantic",
        "dotenv"

    ],
    entry_points={
        "console_scripts": [],
    },
)
