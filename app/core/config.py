from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str = "sua_chave_secreta_super_segura_aqui_para_jwt"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = "sqlite+aiosqlite:///./bank.db"

    class Config:
        env_file = ".env"

settings = Settings()
