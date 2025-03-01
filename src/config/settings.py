from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_name: str = Field(env='DB_NAME')
    db_host: str = Field(env='DB_HOST')
    db_username: str = Field(env='DB_USERNAME')
    db_password: str = Field(env='DB_PASSWORD')

    open_api_key: str = Field(env='OPEN_API_KEY')

    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8')


settings = Settings()
