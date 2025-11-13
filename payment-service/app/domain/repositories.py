from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Payment


class PaymentRepository(ABC):
    @abstractmethod
    async def create(self, payment: Payment) -> Payment: ...

    @abstractmethod
    async def get(self, payment_id: str) -> Optional[Payment]: ...

    @abstractmethod
    async def list_by_user(self, user_id: str) -> List[Payment]: ...

    @abstractmethod
    async def list_by_tournament(self, tournament_id: str) -> List[Payment]: ...

    @abstractmethod
    async def update(self, payment: Payment) -> Payment: ...


class PaymentProcessor(ABC):

    @abstractmethod
    async def charge(self, amount: float, payment_details: dict) -> dict: ...

    @abstractmethod
    async def payout(self, recipient_id: str, amount: float) -> dict: ...