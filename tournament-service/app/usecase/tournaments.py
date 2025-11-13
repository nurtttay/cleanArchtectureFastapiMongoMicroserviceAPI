from typing import List
from datetime import datetime
from ..domain.entities import Tournament, Participant, TournamentStatus, TournamentFormat
from ..domain.repositories import TournamentRepository


class TournamentService:
    def __init__(self, repo: TournamentRepository):
        self.repo = repo

    async def create_tournament(self, name: str, sport_type: str,
                                format_str: str, max_participants: int,
                                organizer_id: str) -> Tournament:
        if not name or max_participants <= 0:
            raise ValueError("Invalid tournament data")

        try:
            format_enum = TournamentFormat(format_str)
        except ValueError:
            raise ValueError("Invalid tournament format")

        tournament = Tournament(
            name=name,
            sport_type=sport_type,
            format=format_enum,
            max_participants=max_participants,
            organizer_id=organizer_id
        )
        return await self.repo.create(tournament)

    async def open_tournament(self, tournament_id: str, organizer_id: str) -> Tournament:
        tournament = await self.repo.get(tournament_id)
        if not tournament:
            raise KeyError("not found")
        if tournament.organizer_id != organizer_id:
            raise ValueError("Not authorized")

        tournament.open_for_registration()
        return await self.repo.update(tournament)

    async def register_participant(self, tournament_id: str, user_id: str, name: str) -> Tournament:
        tournament = await self.repo.get(tournament_id)
        if not tournament:
            raise KeyError("not found")

        if not tournament.can_register():
            raise ValueError("Cannot register")

        for p in tournament.participants:
            if p.user_id == user_id:
                raise ValueError("Already registered")

        tournament.participants.append(Participant(user_id=user_id, name=name))
        tournament.updated_at = datetime.utcnow()

        return await self.repo.update(tournament)

    async def list_tournaments(self) -> List[Tournament]:
        return await self.repo.list()

    async def list_open_tournaments(self) -> List[Tournament]:
        return await self.repo.list_open()

    async def get_tournament(self, tournament_id: str) -> Tournament:
        tournament = await self.repo.get(tournament_id)
        if not tournament:
            raise KeyError("not found")
        return tournament

