from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class TransactionType(Enum):
    TOURNAMENT_FEE = "tournament_fee"
    PAYOUT_VENUE = "payout_venue"
    PAYOUT_WINNER = "payout_winner"


@dataclass
class Payment:
    user_id: str
    tournament_id: str
    amount: float
    transaction_type: TransactionType
    id: Optional[str] = None
    status: PaymentStatus = PaymentStatus.PENDING
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    def mark_completed(self, transaction_id: str):
        if self.status != PaymentStatus.PENDING:
            raise ValueError("Can only complete pending payments")
        self.status = PaymentStatus.COMPLETED
        self.transaction_id = transaction_id
        self.completed_at = datetime.utcnow()

    def mark_failed(self):
        if self.status == PaymentStatus.COMPLETED:
            raise ValueError("Cannot fail completed payment")
        self.status = PaymentStatus.FAILED
