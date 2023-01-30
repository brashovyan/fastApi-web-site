import os
from pydantic import BaseSettings
from dotenv import load_dotenv
load_dotenv()

# имя и бд меняется в .env
class Settings(BaseSettings):
    app_name = os.getenv('NAME_APP')
    db_url = os.getenv('SQLALCHEMY_DATABASE_URL')

    class Config:
        env_file: str = '../.env'


settings = Settings()