import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())

class Settings(BaseSettings):

    postgres_db: str = os.getenv("POSTGRES_DB",'')
    postgres_user: str = os.getenv("POSTGRES_USER",'')
    postgres_password: str = os.getenv("POSTGRES_PASSWORD",'')
    postgres_host: str = os.getenv("POSTGRES_HOST",'')
    jwt_secret: str = os.getenv("JWT_SECRET",'')
    sudo_passwd: str = os.getenv("SUDO_PASSWD", "password")
    dploy_blacklist_zone: str = os.getenv(
        "DPLOY_BLACKLIST_ZONE", "dploy_blacklist")

    postgres_url: str = (f"postgresql+psycopg2://{postgres_user}:{postgres_password}"
        f"@{postgres_host}/{postgres_db}")
    
    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__class__.__name__
    

settings = Settings()