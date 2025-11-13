from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from .schemas import TournamentIn, TournamentOut, ParticipantOut, RegisterParticipantIn
from .auth_router import get_current_user

router = APIRouter()

def get_tournament_service(request: Request):
    return request.app.container.tournament_service

@router.post("/", response_model=TournamentOut)
async def create_tournament(body: TournamentIn, user=Depends(get_current_user),
                           svc=Depends(get_tournament_service)):
    try:
        t = await svc.create_tournament(body.name, body.sport_type, body.format,
                                        body.max_participants, user)
        return TournamentOut(
            id=t.id, name=t.name, sport_type=t.sport_type,
            format=t.format.value, max_participants=t.max_participants,
            organizer_id=t.organizer_id, status=t.status.value,
            participants=[
                ParticipantOut(id=p.id, user_id=p.user_id, name=p.name,
                             registration_date=p.registration_date)
                for p in t.participants
            ],
            created_at=t.created_at, updated_at=t.updated_at
        )
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/", response_model=List[TournamentOut])
async def list_tournaments(open_only: bool = False, svc=Depends(get_tournament_service)):
    tournaments = await svc.list_open_tournaments() if open_only else await svc.list_tournaments()
    return [
        TournamentOut(
            id=t.id, name=t.name, sport_type=t.sport_type,
            format=t.format.value, max_participants=t.max_participants,
            organizer_id=t.organizer_id, status=t.status.value,
            participants=[
                ParticipantOut(id=p.id, user_id=p.user_id, name=p.name,
                             registration_date=p.registration_date)
                for p in t.participants
            ],
            created_at=t.created_at, updated_at=t.updated_at
        )
        for t in tournaments
    ]

@router.get("/{tournament_id}", response_model=TournamentOut)
async def get_tournament(tournament_id: str, svc=Depends(get_tournament_service)):
    try:
        t = await svc.get_tournament(tournament_id)
        return TournamentOut(
            id=t.id, name=t.name, sport_type=t.sport_type,
            format=t.format.value, max_participants=t.max_participants,
            organizer_id=t.organizer_id, status=t.status.value,
            participants=[
                ParticipantOut(id=p.id, user_id=p.user_id, name=p.name,
                             registration_date=p.registration_date)
                for p in t.participants
            ],
            created_at=t.created_at, updated_at=t.updated_at
        )
    except KeyError:
        raise HTTPException(404, "not found")

@router.post("/{tournament_id}/open", response_model=TournamentOut)
async def open_tournament(tournament_id: str, user=Depends(get_current_user),
                         svc=Depends(get_tournament_service)):
    try:
        t = await svc.open_tournament(tournament_id, user)
        return TournamentOut(
            id=t.id, name=t.name, sport_type=t.sport_type,
            format=t.format.value, max_participants=t.max_participants,
            organizer_id=t.organizer_id, status=t.status.value,
            participants=[
                ParticipantOut(id=p.id, user_id=p.user_id, name=p.name,
                             registration_date=p.registration_date)
                for p in t.participants
            ],
            created_at=t.created_at, updated_at=t.updated_at
        )
    except KeyError:
        raise HTTPException(404, "not found")
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/{tournament_id}/register", response_model=TournamentOut)
async def register_participant(tournament_id: str, body: RegisterParticipantIn,
                              user=Depends(get_current_user),
                              svc=Depends(get_tournament_service)):
    try:
        t = await svc.register_participant(tournament_id, user, body.name)
        return TournamentOut(
            id=t.id, name=t.name, sport_type=t.sport_type,
            format=t.format.value, max_participants=t.max_participants,
            organizer_id=t.organizer_id, status=t.status.value,
            participants=[
                ParticipantOut(id=p.id, user_id=p.user_id, name=p.name,
                             registration_date=p.registration_date)
                for p in t.participants
            ],
            created_at=t.created_at, updated_at=t.updated_at
        )
    except KeyError:
        raise HTTPException(404, "not found")
    except ValueError as e:
        raise HTTPException(400, str(e))