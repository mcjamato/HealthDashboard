from __future__ import annotations

from typing import Any

from configuration.intake_fields import BOOLEAN_FIELDS, INTAKE_KEYS
from database.database import DatabaseManager


class ClientIntakeRepository:
    """Stores the full wellness intake questionnaire for one client."""

    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def get_for_client(self, client_id: int) -> dict | None:
        with self.db.connection() as connection:
            row = connection.execute(
                "SELECT * FROM client_intake_profiles WHERE client_id = ? LIMIT 1",
                (client_id,),
            ).fetchone()
        return dict(row) if row else None

    def upsert(self, client_id: int, values: dict[str, Any]) -> None:
        clean = {}
        for key in INTAKE_KEYS:
            value = values.get(key)
            if key in BOOLEAN_FIELDS:
                value = 1 if bool(value) else 0
            elif isinstance(value, list):
                value = "; ".join(str(item) for item in value)
            elif value == "":
                value = None
            clean[key] = value

        columns = ["client_id", *INTAKE_KEYS]
        params = [client_id, *[clean[key] for key in INTAKE_KEYS]]
        insert_columns = ", ".join(columns)
        placeholders = ", ".join("?" for _ in columns)
        updates = ", ".join(f"{key}=excluded.{key}" for key in INTAKE_KEYS)

        sql = f"""
        INSERT INTO client_intake_profiles ({insert_columns})
        VALUES ({placeholders})
        ON CONFLICT(client_id) DO UPDATE SET
            {updates},
            updated_at = CURRENT_TIMESTAMP
        """

        with self.db.connection() as connection:
            connection.execute(sql, params)
