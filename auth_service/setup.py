from setuptools import setup, find_packages

setup(
    name="auth_service",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["uvicorn==0.35.0", "errorhub==0.1.0"],
    entry_points={
        "console_scripts": [],
    },
)
