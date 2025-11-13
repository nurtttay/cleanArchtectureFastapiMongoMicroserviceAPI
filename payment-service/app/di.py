from typing import Optional
from app.infrastructure.db import Database
from app.infrastructure.security import AuthService
from app.infrastructure.fake_payment_processor import FakePaymentProcessor
from app.adapters.repo.mongo_payment_repo import MongoPaymentRepository
from app.usecase.payments import PaymentService

class Container:
    def __init__(self):
        self._db: Optional[Database] = None
        self._auth: Optional[AuthService] = None
        self._payment_service: Optional[PaymentService] = None
        self._payment_processor: Optional[FakePaymentProcessor] = None

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
    def payment_processor(self) -> FakePaymentProcessor:
        if self._payment_processor is None:
            self._payment_processor = FakePaymentProcessor()
        return self._payment_processor

    @property
    def payment_service(self) -> PaymentService:
        if self._payment_service is None:
            self._payment_service = PaymentService(
                MongoPaymentRepository(self.db),
                self.payment_processor
            )
        return self._payment_service
