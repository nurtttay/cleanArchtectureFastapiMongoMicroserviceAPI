from ..domain.repositories import PaymentProcessor
import uuid


class FakePaymentProcessor(PaymentProcessor):

    async def charge(self, amount: float, payment_details: dict) -> dict:
        return {
            "success": True,
            "transaction_id": f"fake_txn_{uuid.uuid4().hex[:8]}",
            "amount": amount
        }

    async def payout(self, recipient_id: str, amount: float) -> dict:
        return {
            "success": True,
            "transaction_id": f"fake_payout_{uuid.uuid4().hex[:8]}"
        }