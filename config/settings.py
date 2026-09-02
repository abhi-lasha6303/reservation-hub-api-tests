import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    BASE_URL = os.getenv("BASE_URL")
    USERNAME = os.getenv("RH_USERNAME")
    PASSWORD = os.getenv("RH_PASSWORD")
    TIMEOUT = int(os.getenv("TIMEOUT", "10"))


settings = Settings()