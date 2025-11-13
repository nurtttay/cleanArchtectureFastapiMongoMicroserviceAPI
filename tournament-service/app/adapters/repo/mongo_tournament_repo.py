from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from ...domain.entities import Tournament, Participant, TournamentStatus, TournamentFormat
from ...domain.repositories import TournamentRepository
from ...infrastructure.db import Database


class MongoTournamentRepository(TournamentRepository):
    def __init__(self, db: Database):
        self.db = db

    async def _coll(self):
        d = await self.db.db()
        return d.get_collection("tournaments")

    def _map(self, d) -> Tournament:
        participants = [
            Participant(
                id=str(i),
                user_id=p["user_id"],
                name=p["name"],
                registration_date=p.get("registration_date", datetime.utcnow())
            )
            for i, p in enumerate(d.get("participants", []))
        ]

        return Tournament(
            id=str(d["_id"]),
            name=d["name"],
            sport_type=d["sport_type"],
            format=TournamentFormat(d["format"]),
            max_participants=d["max_participants"],
            organizer_id=d["organizer_id"],
            status=TournamentStatus(d["status"]),
            participants=participants,
            created_at=d["created_at"],
            updated_at=d["updated_at"]
        )

    async def create(self, tournament: Tournament) -> Tournament:
        coll = await self._coll()
        doc = {
            "name": tournament.name,
            "sport_type": tournament.sport_type,
            "format": tournament.format.value,
            "max_participants": tournament.max_participants,
            "organizer_id": tournament.organizer_id,
            "status": tournament.status.value,
            "participants": [],
            "created_at": tournament.created_at,
            "updated_at": tournament.updated_at,
        }
        res = await coll.insert_one(doc)
        tournament.id = str(res.inserted_id)
        return tournament

    async def get(self, tournament_id: str) -> Optional[Tournament]:
        try:
            oid = ObjectId(tournament_id)
        except Exception:
            return None
        coll = await self._coll()
        d = await coll.find_one({"_id": oid})
        return self._map(d) if d else None

    async def list(self) -> List[Tournament]:
        coll = await self._coll()
        tournaments: List[Tournament] = []
        async for d in coll.find({}).sort("created_at", -1):
            tournaments.append(self._map(d))
        return tournaments

    async def list_open(self) -> List[Tournament]:
        coll = await self._coll()
        tournaments: List[Tournament] = []
        async for d in coll.find({"status": "open"}).sort("created_at", -1):
            tournaments.append(self._map(d))
        return tournaments

    async def update(self, tournament: Tournament) -> Tournament:
        coll = await self._coll()
        oid = ObjectId(tournament.id)
        await coll.update_one({"_id": oid}, {"$set": {
            "name": tournament.name,
            "status": tournament.status.value,
            "participants": [
                {
                    "user_id": p.user_id,
                    "name": p.name,
                    "registration_date": p.registration_date
                }
                for p in tournament.participants
            ],
            "updated_at": tournament.updated_at,
        }})
        return tournament

    async def delete(self, tournament_id: str) -> bool:
        coll = await self._coll()
        try:
            oid = ObjectId(tournament_id)
        except Exception:
            return False
        res = await coll.delete_one({"_id": oid})
        return bool(res.deleted_count)
