from abc import ABC, abstractmethod
from typing import List, Optional
from .entities import Tournament


class TournamentRepository(ABC):
    @abstractmethod
    async def create(self, tournament: Tournament) -> Tournament: ...

    @abstractmethod
    async def get(self, tournament_id: str) -> Optional[Tournament]: ...

    @abstractmethod
    async def list(self) -> List[Tournament]: ...

    @abstractmethod
    async def list_open(self) -> List[Tournament]: ...

    @abstractmethod
    async def update(self, tournament: Tournament) -> Tournament: ...

    @abstractmethod
    async def delete(self, tournament_id: str) -> bool: ...