from __future__ import annotations

from typing import Any

import pandas as pd

from database.database import DatabaseManager


class DomainRepository:
    table_name: str
    columns: tuple[str, ...]

    def __init__(self, db: DatabaseManager) -> None:
        self.db = db

    def create(self, values: dict[str, Any]) -> int:
        missing = [column for column in self.columns if column not in values]
        if missing:
            raise ValueError(f"Missing repository values: {missing}")

        placeholders = ", ".join("?" for _ in self.columns)
        column_sql = ", ".join(self.columns)
        sql = f"INSERT INTO {self.table_name} ({column_sql}) VALUES ({placeholders})"

        with self.db.connection() as connection:
            cursor = connection.execute(
                sql,
                tuple(values[column] for column in self.columns),
            )
            return int(cursor.lastrowid)

    def list_for_client(self, client_id: int) -> pd.DataFrame:
        with self.db.connection() as connection:
            return pd.read_sql_query(
                f'''
                SELECT *
                FROM {self.table_name}
                WHERE client_id = ? AND is_active = 1
                ORDER BY recorded_on DESC, id DESC
                ''',
                connection,
                params=(client_id,),
            )

    def deactivate(self, record_id: int) -> None:
        with self.db.connection() as connection:
            connection.execute(
                f"UPDATE {self.table_name} SET is_active = 0 WHERE id = ?",
                (record_id,),
            )


class ExerciseRepository(DomainRepository):
    table_name = "exercise_records"
    columns = (
        "client_id", "recorded_on", "exercise_type", "duration_minutes",
        "intensity", "steps", "distance_km", "calories_burned", "notes",
    )


class HealthRepository(DomainRepository):
    table_name = "health_records"
    columns = (
        "client_id", "recorded_on", "weight_kg", "sleep_hours",
        "sleep_quality", "resting_heart_rate", "systolic_bp",
        "diastolic_bp", "water_liters", "notes",
    )


class MentalWellnessRepository(DomainRepository):
    table_name = "mental_wellness_records"
    columns = (
        "client_id", "recorded_on", "mood_score", "stress_score",
        "energy_score", "focus_score", "meditation_minutes", "journal_entry",
    )


class NutritionRepository(DomainRepository):
    table_name = "nutrition_records"
    columns = (
        "client_id", "recorded_on", "meal_type", "calories",
        "protein_g", "carbs_g", "fat_g", "fiber_g", "water_liters", "notes",
    )
