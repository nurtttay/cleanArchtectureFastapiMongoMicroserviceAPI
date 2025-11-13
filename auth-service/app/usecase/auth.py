from typing import Dict, Optional
from datetime import datetime
from ..domain.entities import User
from ..domain.repositories import UserRepository


class AuthService:
    def __init__(self, repo: UserRepository, security_service):
        self.repo = repo
        self.security = security_service

    async def signup(self, email: str, password: str, full_name: Optional[str] = None) -> Dict[str, str]:

        existing = await self.repo.get_by_email(email)
        if existing:
            raise ValueError("User with this email already exists")

        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")

        password_hash = self.security.hash_password(password)
        user = User(
            email=email,
            password_hash=password_hash,
            full_name=full_name,
            is_active=True,
            is_verified=False
        )


        saved_user = await self.repo.create(user)

        access_token = self.security.create_access_token({"sub": saved_user.email, "user_id": saved_user.id})
        refresh_token = self.security.create_refresh_token({"sub": saved_user.email, "user_id": saved_user.id})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": saved_user.id,
            "email": saved_user.email
        }

    async def login(self, email: str, password: str) -> Dict[str, str]:

        user = await self.repo.get_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("Account is deactivated")

        if not self.security.verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        user.mark_login()
        await self.repo.update(user)

        access_token = self.security.create_access_token({"sub": user.email, "user_id": user.id})
        refresh_token = self.security.create_refresh_token({"sub": user.email, "user_id": user.id})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": user.id,
            "email": user.email
        }

    async def refresh_token(self, refresh_token: str) -> Dict[str, str]:

        try:
            payload = self.security.decode_refresh_token(refresh_token)
            email = payload.get("sub")
            user_id = payload.get("user_id")

            user = await self.repo.get_by_email(email)
            if not user or not user.is_active:
                raise ValueError("Invalid refresh token")

            access_token = self.security.create_access_token({"sub": email, "user_id": user_id})

            return {
                "access_token": access_token,
                "token_type": "bearer"
            }
        except Exception:
            raise ValueError("Invalid refresh token")

    async def verify_token(self, token: str) -> Dict[str, str]:

        try:
            payload = self.security.decode_token(token)
            email = payload.get("sub")
            user_id = payload.get("user_id")

            # Verify user exists
            user = await self.repo.get_by_email(email)
            if not user or not user.is_active:
                raise ValueError("Invalid token")

            return {
                "email": email,
                "user_id": user_id,
                "is_verified": user.is_verified
            }
        except Exception:
            raise ValueError("Invalid or expired token")

    async def get_user_profile(self, user_id: str) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise KeyError("User not found")
        return user

    async def update_profile(self, user_id: str, full_name: Optional[str] = None) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise KeyError("User not found")

        if full_name:
            user.full_name = full_name
            user.updated_at = datetime.utcnow()

        return await self.repo.update(user)

    async def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise KeyError("User not found")

        if not self.security.verify_password(old_password, user.password_hash):
            raise ValueError("Current password is incorrect")

        if len(new_password) < 6:
            raise ValueError("New password must be at least 6 characters")

        user.password_hash = self.security.hash_password(new_password)
        user.updated_at = datetime.utcnow()
        await self.repo.update(user)

        return True