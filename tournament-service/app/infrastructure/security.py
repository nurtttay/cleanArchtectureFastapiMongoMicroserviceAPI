import os
import hashlib
from datetime import datetime, timedelta
from jose import jwt

class AuthService:
    def __init__(self):
        self.users = {}  # In-memory user store
        self.secret = os.getenv("JWT_SECRET", "akezhan_is_very_handsome")
        self.algorithm = os.getenv("JWT_ALG", "HS256")
        self.expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    def hash_password(self, password: str) -> str:
        return hashlib.pbkdf2_hmac("sha256", password.encode(), b"salt", 100000).hex()

    def verify_password(self, plain: str, hashed: str) -> bool:
        return self.hash_password(plain) == hashed

    def create_access_token(self, email: str) -> str:
        expire = datetime.utcnow() + timedelta(minutes=self.expire_minutes)
        payload = {"sub": email, "exp": expire}
        return jwt.encode(payload, self.secret, algorithm=self.algorithm)

    def decode_token(self, token: str) -> dict:
        return jwt.decode(token, self.secret, algorithms=[self.algorithm])