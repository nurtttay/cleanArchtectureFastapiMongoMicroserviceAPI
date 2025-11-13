from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from .schemas import PaymentIn, PaymentOut
from .auth_router import get_current_user

router = APIRouter()

def get_payment_service(request: Request):
    return request.app.container.payment_service  # type: ignore[attr-defined]

@router.post("/", response_model=PaymentOut)
async def process_payment(body: PaymentIn, user=Depends(get_current_user),
                         svc=Depends(get_payment_service)):
    try:
        payment_details = {
            "method": body.payment_method,
            "card_number": body.card_number
        }
        p = await svc.process_tournament_fee(user, body.tournament_id, body.amount, payment_details)
        return PaymentOut(
            id=p.id, user_id=p.user_id, tournament_id=p.tournament_id,
            amount=p.amount, transaction_type=p.transaction_type.value,
            status=p.status.value, payment_method=p.payment_method,
            transaction_id=p.transaction_id, created_at=p.created_at,
            completed_at=p.completed_at
        )
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/history", response_model=List[PaymentOut])
async def get_payment_history(user=Depends(get_current_user), svc=Depends(get_payment_service)):
    payments = await svc.get_user_payments(user)
    return [
        PaymentOut(
            id=p.id, user_id=p.user_id, tournament_id=p.tournament_id,
            amount=p.amount, transaction_type=p.transaction_type.value,
            status=p.status.value, payment_method=p.payment_method,
            transaction_id=p.transaction_id, created_at=p.created_at,
            completed_at=p.completed_at
        )
        for p in payments
    ]

@router.get("/{payment_id}", response_model=PaymentOut)
async def get_payment(payment_id: str, user=Depends(get_current_user),
                     svc=Depends(get_payment_service)):
    try:
        p = await svc.get_payment(payment_id)
        if p.user_id != user:
            raise HTTPException(403, "Not authorized")
        return PaymentOut(
            id=p.id, user_id=p.user_id, tournament_id=p.tournament_id,
            amount=p.amount, transaction_type=p.transaction_type.value,
            status=p.status.value, payment_method=p.payment_method,
            transaction_id=p.transaction_id, created_at=p.created_at,
            completed_at=p.completed_at
        )
    except KeyError:
        raise HTTPException(404, "not found")
