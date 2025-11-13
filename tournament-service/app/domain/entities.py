from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class TournamentStatus(Enum):
    DRAFT = "draft"
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TournamentFormat(Enum):
    SINGLE_ELIMINATION = "single_elimination"
    DOUBLE_ELIMINATION = "double_elimination"
    ROUND_ROBIN = "round_robin"


@dataclass
class Participant:
    user_id: str
    name: str
    id: Optional[str] = None
    registration_date: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Tournament:
    name: str
    sport_type: str
    format: TournamentFormat
    max_participants: int
    organizer_id: str
    id: Optional[str] = None
    status: TournamentStatus = TournamentStatus.DRAFT
    participants: List[Participant] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def can_register(self) -> bool:
        return (self.status == TournamentStatus.OPEN and
                len(self.participants) < self.max_participants)

    def open_for_registration(self):
        if self.status != TournamentStatus.DRAFT:
            raise ValueError("Can only open draft tournaments")
        self.status = TournamentStatus.OPEN
        self.updated_at = datetime.utcnow()