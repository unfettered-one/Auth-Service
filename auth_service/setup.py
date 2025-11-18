"""
Setup and dependencies for the Auth-Service.
"""

from setuptools import setup, find_packages

setup(
    name="auth_service",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "uvicorn==0.35.0",
        "errorhub==0.1.9",
        "bcrypt==4.3.0",
        "email_validator==2.2.0",
        "orjson==3.11.4",
        "PyJWT==2.10.1",
    ],
    extras_require={"dev": ["pylint"]},
    entry_points={
        "console_scripts": [],
    },
)
