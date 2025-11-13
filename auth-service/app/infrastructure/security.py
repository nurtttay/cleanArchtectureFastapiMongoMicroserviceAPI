import os
import hashlib
from datetime import datetime, timedelta
from jose import jwt, JWTError


class SecurityService:
    def __init__(self):
        self.secret = os.getenv("JWT_SECRET", "nurtay_is_very_cool_and_handsome")
        self.algorithm = os.getenv("JWT_ALG", "HS256")
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.refresh_token_expire_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    def hash_password(self, password: str) -> str:
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            b'salt_should_be_random_per_user',  # In production: use unique salt per user
            100000
        ).hex()

    def verify_password(self, plain: str, hashed: str) -> bool:
        return self.hash_password(plain) == hashed

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, self.secret, algorithm=self.algorithm)

    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, self.secret, algorithm=self.algorithm)

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            if payload.get("type") != "access":
                raise JWTError("Invalid token type")
            return payload
        except JWTError as e:
            raise ValueError(f"Invalid token: {str(e)}")

    def decode_refresh_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            if payload.get("type") != "refresh":
                raise JWTError("Invalid token type")
            return payload
        except JWTError as e:
            raise ValueError(f"Invalid refresh token: {str(e)}")