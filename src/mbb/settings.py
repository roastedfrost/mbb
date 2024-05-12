from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_name: str
    host: str
    port: int
    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
