
from typing import List, Optional
from bson import ObjectId
from ...domain.entities import Payment, PaymentStatus, TransactionType
from ...domain.repositories import PaymentRepository
from ...infrastructure.db import Database

class MongoPaymentRepository(PaymentRepository):
    def __init__(self, db: Database):
        self.db = db

    async def _coll(self):
        d = await self.db.db()
        return d.get_collection("payments")

    def _map(self, d) -> Payment:
        return Payment(
            id=str(d["_id"]),
            user_id=d["user_id"],
            tournament_id=d["tournament_id"],
            amount=d["amount"],
            transaction_type=TransactionType(d["transaction_type"]),
            status=PaymentStatus(d["status"]),
            payment_method=d.get("payment_method"),
            transaction_id=d.get("transaction_id"),
            created_at=d["created_at"],
            completed_at=d.get("completed_at")
        )

    async def create(self, payment: Payment) -> Payment:
        coll = await self._coll()
        doc = {
            "user_id": payment.user_id,
            "tournament_id": payment.tournament_id,
            "amount": payment.amount,
            "transaction_type": payment.transaction_type.value,
            "status": payment.status.value,
            "payment_method": payment.payment_method,
            "transaction_id": payment.transaction_id,
            "created_at": payment.created_at,
            "completed_at": payment.completed_at
        }
        res = await coll.insert_one(doc)
        payment.id = str(res.inserted_id)
        return payment

    async def get(self, payment_id: str) -> Optional[Payment]:
        try:
            oid = ObjectId(payment_id)
        except Exception:
            return None
        coll = await self._coll()
        d = await coll.find_one({"_id": oid})
        return self._map(d) if d else None

    async def list_by_user(self, user_id: str) -> List[Payment]:
        coll = await self._coll()
        payments: List[Payment] = []
        async for d in coll.find({"user_id": user_id}).sort("created_at", -1):
            payments.append(self._map(d))
        return payments

    async def list_by_tournament(self, tournament_id: str) -> List[Payment]:
        coll = await self._coll()
        payments: List[Payment] = []
        async for d in coll.find({"tournament_id": tournament_id}).sort("created_at", -1):
            payments.append(self._map(d))
        return payments

    async def update(self, payment: Payment) -> Payment:
        coll = await self._coll()
        oid = ObjectId(payment.id)
        await coll.update_one({"_id": oid}, {"$set": {
            "status": payment.status.value,
            "transaction_id": payment.transaction_id,
            "completed_at": payment.completed_at
        }})
        return payment
