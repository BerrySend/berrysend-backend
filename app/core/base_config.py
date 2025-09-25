from pydantic.v1 import BaseSettings

"""
    Base configuration class for the application using Pydantic's BaseSettings.
"""
class BaseConfig(BaseSettings):
    APP_HOST: str
    APP_PORT: int
    DATABASE_NAME: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create an instance of BaseConfig
config = BaseConfig()