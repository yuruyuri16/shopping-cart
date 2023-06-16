from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_PORT: int
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_HOSTNAME: str

    class Config:
        env_file = './.env'


settings = Settings(DATABASE_PORT=6500, POSTGRES_PASSWORD='examplepassword', POSTGRES_USER='exampleusername', POSTGRES_DB='examplename', POSTGRES_HOST='examplehostname', POSTGRES_HOSTNAME='127.0.0.1')
