from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Благотворительный фонд QRKot'
    database_url: str = 'sqlite+aiosqlite:///./charity.db'
    secret: str = 'SECRET_KEY'

    class Config:
        env_file = '.env'


settings = Settings()
