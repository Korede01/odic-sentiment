from pydantic import BaseSettings


class Settings(BaseSettings):
    repo_id: str
    model_filename: str
    vectorizer_filename: str
    access_token_write: int
    access_token_read: str
    database_password: str
    version: str
    cors_1: str
    cors_2: str

    class Config:
        env_file = ".env"


settings = Settings()