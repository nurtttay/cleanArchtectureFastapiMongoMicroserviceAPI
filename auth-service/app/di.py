from typing import Optional
from app.infrastructure.db import Database
from app.infrastructure.security import SecurityService
from app.adapters.repo.mongo_user_repo import MongoUserRepository
from app.usecase.auth import AuthService


class Container:
    def __init__(self):
        self._db: Optional[Database] = None
        self._security: Optional[SecurityService] = None
        self._user_repo: Optional[MongoUserRepository] = None
        self._auth_service: Optional[AuthService] = None

    @property
    def db(self) -> Database:
        if self._db is None:
            self._db = Database()
        return self._db

    @property
    def security(self) -> SecurityService:
        if self._security is None:
            self._security = SecurityService()
        return self._security

    @property
    def user_repo(self) -> MongoUserRepository:
        if self._user_repo is None:
            self._user_repo = MongoUserRepository(self.db)
        return self._user_repo

    @property
    def auth_service(self) -> AuthService:
        if self._auth_service is None:
            self._auth_service = AuthService(self.user_repo, self.security)
        return self._auth_service
