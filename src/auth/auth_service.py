from __future__ import annotations

import bcrypt

from repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    @staticmethod
    def hash_password(password: str) -> str:
        if len(password) < 8:
            raise ValueError("Password must contain at least 8 characters.")
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"),
                password_hash.encode("utf-8"),
            )
        except (ValueError, TypeError):
            return False

    def authenticate(self, username: str, password: str) -> dict | None:
        user = self.repository.find_by_username(username)
        if user is None:
            return None
        if not self.verify_password(password, user["password_hash"]):
            return None
        return {
            "user_id": int(user["id"]),
            "username": user["username"],
            "role": user["role"],
            "client_id": (
                int(user["client_id"]) if user["client_id"] is not None else None
            ),
        }

    def ensure_initial_admin(self, username: str, password: str) -> bool:
        if self.repository.count_admins() > 0:
            return False
        self.repository.create(
            username=username,
            password_hash=self.hash_password(password),
            role="admin",
            client_id=None,
        )
        return True
