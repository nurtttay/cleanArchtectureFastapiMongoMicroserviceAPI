import os

class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "tournament-service")  # or "payment-service"
    DB_NAME: str = os.getenv("DB_NAME", "tournamentdb")  # or "paymentdb"
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/?replicaSet=rs0")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "and_also_here")
    JWT_ALG: str = os.getenv("JWT_ALG", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:8080")

settings = Settings()