from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class TournamentIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    sport_type: str
    format: str  # single_elimination, double_elimination, round_robin
    max_participants: int = Field(..., gt=0)

class ParticipantOut(BaseModel):
    id: str
    user_id: str
    name: str
    registration_date: datetime

class TournamentOut(BaseModel):
    id: str
    name: str
    sport_type: str
    format: str
    max_participants: int
    organizer_id: str
    status: str
    participants: List[ParticipantOut]
    created_at: datetime
    updated_at: datetime

class RegisterParticipantIn(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)