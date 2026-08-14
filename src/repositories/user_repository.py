from __future__ import annotations

import pandas as pd

from database.database import DatabaseManager


class UserRepository:
    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def create(
        self,
        username: str,
        password_hash: str,
        role: str,
        client_id: int | None = None,
    ) -> int:
        if role not in {"admin", "client"}:
            raise ValueError("Role must be admin or client.")
        if role == "client" and client_id is None:
            raise ValueError("Client accounts must be linked to a client.")

        with self.db.connection() as connection:
            cursor = connection.execute(
                '''
                INSERT INTO users(username, password_hash, role, client_id)
                VALUES (?, ?, ?, ?)
                ''',
                (username.strip().lower(), password_hash, role, client_id),
            )
            return int(cursor.lastrowid)

    def find_by_username(self, username: str) -> dict | None:
        with self.db.connection() as connection:
            row = connection.execute(
                '''
                SELECT id, username, password_hash, role, client_id, active, created_at
                FROM users
                WHERE username = ? AND active = 1
                LIMIT 1
                ''',
                (username.strip().lower(),),
            ).fetchone()
        return dict(row) if row else None

    def list_active(self) -> pd.DataFrame:
        with self.db.connection() as connection:
            return pd.read_sql_query(
                '''
                SELECT
                    users.id,
                    users.username,
                    users.role,
                    users.client_id,
                    CASE
                        WHEN users.client_id IS NULL THEN 'Administrator'
                        ELSE clients.first_name || ' ' || clients.last_name
                    END AS client,
                    users.created_at
                FROM users
                LEFT JOIN clients ON clients.id = users.client_id
                WHERE users.active = 1
                ORDER BY users.role, users.username
                ''',
                connection,
            )

    def deactivate(self, user_id: int) -> None:
        with self.db.connection() as connection:
            connection.execute(
                "UPDATE users SET active = 0 WHERE id = ?",
                (user_id,),
            )

    def count_admins(self) -> int:
        with self.db.connection() as connection:
            return int(
                connection.execute(
                    "SELECT COUNT(*) FROM users WHERE role='admin' AND active=1"
                ).fetchone()[0]
            )
