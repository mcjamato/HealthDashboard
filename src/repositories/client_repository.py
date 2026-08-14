from __future__ import annotations

import pandas as pd

from database.database import DatabaseManager


class ClientRepository:
    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def create(
        self,
        first_name: str,
        last_name: str,
        email: str,
        birth_date: str | None,
    ) -> int:
        with self.db.connection() as connection:
            cursor = connection.execute(
                '''
                INSERT INTO clients(first_name, last_name, email, birth_date)
                VALUES (?, ?, ?, ?)
                ''',
                (
                    first_name.strip(),
                    last_name.strip(),
                    email.strip().lower() or None,
                    birth_date,
                ),
            )
            return int(cursor.lastrowid)

    def get_by_email(self, email: str) -> dict | None:
        with self.db.connection() as connection:
            row = connection.execute(
                '''
                SELECT id, first_name, last_name, email, birth_date, active, created_at
                FROM clients
                WHERE lower(email) = lower(?)
                LIMIT 1
                ''',
                (email.strip(),),
            ).fetchone()
        return dict(row) if row else None

    def list_active(self) -> pd.DataFrame:
        with self.db.connection() as connection:
            return pd.read_sql_query(
                '''
                SELECT id, first_name, last_name, email, birth_date, created_at
                FROM clients
                WHERE active = 1
                ORDER BY last_name, first_name
                ''',
                connection,
            )

    def deactivate(self, client_id: int) -> None:
        with self.db.connection() as connection:
            connection.execute(
                "UPDATE clients SET active = 0 WHERE id = ?",
                (client_id,),
            )
