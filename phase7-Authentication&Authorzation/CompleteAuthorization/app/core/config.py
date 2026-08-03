from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY:str
    JWT_ALGORITHM:str
    JWT_ACCESS_TOKEN_EXPIRY_MINUTES:int
    JWT_REFRESH_TOKEN_EXPIRY_DAYS:int

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore'
        )

settings = Settings()

    