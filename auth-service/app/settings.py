import os

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Auth Service")
    DB_NAME: str = os.getenv("DB_NAME", "authdb")
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/?replicaSet=rs0")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "nurtay_baimagambetov")
    JWT_ALG: str = os.getenv("JWT_ALG", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")

settings = Settings()