import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BASE_URL = os.getenv("BASE_URL", "https://petstore.swagger.io/v2")
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))
    API_KEY = os.getenv("API_KEY", "special-key")
config = Settings()