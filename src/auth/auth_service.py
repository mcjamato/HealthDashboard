from __future__ import annotations

import bcrypt

from repositories.user_repository import UserRepository


class AuthService:
    """Authentication, password hashing, and password changes."""

    def __init__(
        self,
        repository: UserRepository,
    ) -> None:
        self.repository = repository

    @staticmethod
    def hash_password(
        password: str,
    ) -> str:
        if len(password) < 8:
            raise ValueError(
                "Password must contain at least 8 characters."
            )

        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(),
        ).decode("utf-8")

    @staticmethod
    def verify_password(
        password: str,
        password_hash: str,
    ) -> bool:
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"),
                password_hash.encode("utf-8"),
            )
        except (
            ValueError,
            TypeError,
        ):
            return False

    def authenticate(
        self,
        username: str,
        password: str,
    ) -> dict | None:
        user = self.repository.find_by_username(
            username
        )

        if user is None:
            return None

        if not self.verify_password(
            password,
            user["password_hash"],
        ):
            return None

        return {
            "user_id": int(user["id"]),
            "username": user["username"],
            "role": user["role"],
            "client_id": (
                int(user["client_id"])
                if user["client_id"] is not None
                else None
            ),
        }

    def change_password(
        self,
        user_id: int,
        current_password: str,
        new_password: str,
        confirm_password: str,
    ) -> None:
        if new_password != confirm_password:
            raise ValueError(
                "New passwords do not match."
            )

        user = self.repository.find_by_id(
            user_id
        )

        if user is None:
            raise ValueError(
                "User account was not found."
            )

        if not self.verify_password(
            current_password,
            user["password_hash"],
        ):
            raise ValueError(
                "Current password is incorrect."
            )

        if self.verify_password(
            new_password,
            user["password_hash"],
        ):
            raise ValueError(
                "New password must be different "
                "from the current password."
            )

        self.repository.update_password(
            user_id=user_id,
            password_hash=self.hash_password(
                new_password
            ),
        )

    def reset_password(
        self,
        user_id: int,
        new_password: str,
    ) -> None:
        self.repository.update_password(
            user_id=user_id,
            password_hash=self.hash_password(
                new_password
            ),
        )

    def ensure_initial_admin(
        self,
        username: str,
        password: str,
    ) -> bool:
        if self.repository.count_admins() > 0:
            return False

        self.repository.create(
            username=username,
            password_hash=self.hash_password(
                password
            ),
            role="admin",
            client_id=None,
        )

        return True
