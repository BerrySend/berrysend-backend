from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Class for managing application settings.
    """
    # CSV Files URLs
    MARITIME_PORTS_CSV_URL: str = ""
    AIR_PORTS_CSV_URL: str = ""
    EXPORTS_CSV_URL: str = ""

    # Database-related settings
    MYSQL_USER: str = ""
    MYSQL_PASSWORD: str = ""
    MYSQL_HOST: str = ""
    MYSQL_PORT: int = 0
    MYSQL_DB: str = ""

    # JWT Settings
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = ""
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    def database_url(self) -> str:
        """
        Creates the connection string for the database.

        :return: The connection string.
        """
        return (
            f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
        )

    class Config:
        """
        Configuration for the Settings class.
        """
        env_file = "development.env"
        env_file_encoding = "utf-8"

# Global instance for the Settings class
settings = Settings()