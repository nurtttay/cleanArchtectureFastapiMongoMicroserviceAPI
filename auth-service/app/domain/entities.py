from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    email: str
    password_hash: str
    id: Optional[str] = None
    full_name: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    def mark_login(self):
        self.last_login = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def deactivate(self):
        if not self.is_active:
            raise ValueError("User already inactive")
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def verify_email(self):
        if self.is_verified:
            raise ValueError("Email already verified")
        self.is_verified = True
        self.updated_at = datetime.utcnow()