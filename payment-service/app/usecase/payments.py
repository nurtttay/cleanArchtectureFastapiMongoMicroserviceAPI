from typing import List
from ..domain.entities import Payment, TransactionType, PaymentStatus
from ..domain.repositories import PaymentRepository, PaymentProcessor


class PaymentService:
    def __init__(self, repo: PaymentRepository, processor: PaymentProcessor):
        self.repo = repo
        self.processor = processor

    async def process_tournament_fee(self, user_id: str, tournament_id: str,
                                     amount: float, payment_details: dict) -> Payment:
        if amount <= 0:
            raise ValueError("Invalid amount")

        payment = Payment(
            user_id=user_id,
            tournament_id=tournament_id,
            amount=amount,
            transaction_type=TransactionType.TOURNAMENT_FEE,
            payment_method=payment_details.get("method", "card")
        )

        payment = await self.repo.create(payment)

        result = await self.processor.charge(amount, payment_details)

        if result["success"]:
            payment.mark_completed(result["transaction_id"])
        else:
            payment.mark_failed()

        return await self.repo.update(payment)

    async def get_payment(self, payment_id: str) -> Payment:
        payment = await self.repo.get(payment_id)
        if not payment:
            raise KeyError("not found")
        return payment

    async def get_user_payments(self, user_id: str) -> List[Payment]:
        return await self.repo.list_by_user(user_id)

    async def get_tournament_payments(self, tournament_id: str) -> List[Payment]:
        return await self.repo.list_by_tournament(tournament_id)