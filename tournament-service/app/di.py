from typing import Optional
from app.infrastructure.db import Database
from app.infrastructure.security import AuthService
from app.adapters.repo.mongo_tournament_repo import MongoTournamentRepository
from app.usecase.tournaments import TournamentService

class Container:
    def __init__(self):
        self._db: Optional[Database] = None
        self._auth: Optional[AuthService] = None
        self._tournament_service: Optional[TournamentService] = None

    @property
    def db(self) -> Database:
        if self._db is None:
            self._db = Database()
        return self._db

    @property
    def auth(self) -> AuthService:
        if self._auth is None:
            self._auth = AuthService()
        return self._auth

    @property
    def tournament_service(self) -> TournamentService:
        if self._tournament_service is None:
            self._tournament_service = TournamentService(MongoTournamentRepository(self.db))
        return self._tournament_service
