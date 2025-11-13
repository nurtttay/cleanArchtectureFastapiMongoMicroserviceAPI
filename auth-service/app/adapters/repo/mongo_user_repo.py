from typing import List, Optional
from bson import ObjectId
from ...domain.entities import User
from ...domain.repositories import UserRepository
from ...infrastructure.db import Database


class MongoUserRepository(UserRepository):
    def __init__(self, db: Database):
        self.db = db

    async def _coll(self):
        d = await self.db.db()
        return d.get_collection("users")

    def _map(self, d) -> User:
        return User(
            id=str(d["_id"]),
            email=d["email"],
            password_hash=d["password_hash"],
            full_name=d.get("full_name"),
            is_active=d.get("is_active", True),
            is_verified=d.get("is_verified", False),
            created_at=d["created_at"],
            updated_at=d["updated_at"],
            last_login=d.get("last_login")
        )

    async def create(self, user: User) -> User:
        coll = await self._coll()
        doc = {
            "email": user.email,
            "password_hash": user.password_hash,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "last_login": user.last_login
        }
        res = await coll.insert_one(doc)
        user.id = str(res.inserted_id)
        return user

    async def get_by_id(self, user_id: str) -> Optional[User]:
        try:
            oid = ObjectId(user_id)
        except Exception:
            return None
        coll = await self._coll()
        d = await coll.find_one({"_id": oid})
        return self._map(d) if d else None

    async def get_by_email(self, email: str) -> Optional[User]:
        coll = await self._coll()
        d = await coll.find_one({"email": email})
        return self._map(d) if d else None

    async def update(self, user: User) -> User:
        coll = await self._coll()
        oid = ObjectId(user.id)
        await coll.update_one({"_id": oid}, {"$set": {
            "full_name": user.full_name,
            "password_hash": user.password_hash,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "updated_at": user.updated_at,
            "last_login": user.last_login
        }})
        return user

    async def delete(self, user_id: str) -> bool:
        coll = await self._coll()
        try:
            oid = ObjectId(user_id)
        except Exception:
            return False
        res = await coll.delete_one({"_id": oid})
        return bool(res.deleted_count)

    async def list_all(self) -> List[User]:
        coll = await self._coll()
        users: List[User] = []
        async for d in coll.find({}).sort("created_at", -1):
            users.append(self._map(d))
        return users

