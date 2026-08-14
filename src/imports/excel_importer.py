from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO

import pandas as pd

from repositories.client_repository import ClientRepository


@dataclass
class ImportResult:
    imported: int
    rejected: int
    errors: list[str]


class ExcelImporter:
    SHEETS = {"Clients", "Exercise", "Health", "MentalWellness", "Nutrition"}

    def __init__(self, clients, exercise, health, mental, nutrition) -> None:
        self.clients: ClientRepository = clients
        self.repos = {
            "Exercise": exercise,
            "Health": health,
            "MentalWellness": mental,
            "Nutrition": nutrition,
        }

    @staticmethod
    def template_bytes() -> bytes:
        output = BytesIO()
        sheets = {
            "Clients": [
                "first_name", "last_name", "email", "birth_date"
            ],
            "Exercise": [
                "client_email", "recorded_on", "exercise_type",
                "duration_minutes", "intensity", "steps",
                "distance_km", "calories_burned", "notes"
            ],
            "Health": [
                "client_email", "recorded_on", "weight_kg",
                "sleep_hours", "sleep_quality", "resting_heart_rate",
                "systolic_bp", "diastolic_bp", "water_liters", "notes"
            ],
            "MentalWellness": [
                "client_email", "recorded_on", "mood_score", "stress_score",
                "energy_score", "focus_score", "meditation_minutes",
                "journal_entry"
            ],
            "Nutrition": [
                "client_email", "recorded_on", "meal_type", "calories",
                "protein_g", "carbs_g", "fat_g", "fiber_g",
                "water_liters", "notes"
            ],
        }
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            for name, columns in sheets.items():
                pd.DataFrame(columns=columns).to_excel(
                    writer, sheet_name=name, index=False
                )
        return output.getvalue()

    def _resolve_client_id(self, email: str) -> int:
        client = self.clients.get_by_email(email)
        if client is None:
            raise ValueError(f"Unknown client_email: {email}")
        return int(client["id"])

    def import_workbook(self, content: bytes) -> ImportResult:
        book = pd.ExcelFile(BytesIO(content))
        missing = self.SHEETS.difference(book.sheet_names)
        if missing:
            return ImportResult(0, 0, [f"Missing worksheets: {sorted(missing)}"])

        imported = 0
        rejected = 0
        errors: list[str] = []

        # Clients first: existing email is treated as already known, not duplicated.
        clients_frame = pd.read_excel(book, sheet_name="Clients")
        for index, row in clients_frame.iterrows():
            try:
                first = row.get("first_name")
                last = row.get("last_name")
                email = row.get("email")
                if pd.isna(first) or pd.isna(last) or pd.isna(email):
                    raise ValueError("first_name, last_name, and email are required")

                email_text = str(email).strip().lower()
                existing = self.clients.get_by_email(email_text)

                if existing is None:
                    birth = row.get("birth_date")
                    birth_text = (
                        None
                        if pd.isna(birth)
                        else pd.to_datetime(birth).date().isoformat()
                    )
                    self.clients.create(
                        str(first),
                        str(last),
                        email_text,
                        birth_text,
                    )
                    imported += 1
            except Exception as exc:
                rejected += 1
                errors.append(f"Clients row {index + 2}: {exc}")

        # Domain sheets use stable client_email, then map to database client_id.
        for sheet, repo in self.repos.items():
            frame = pd.read_excel(book, sheet_name=sheet)

            for index, row in frame.iterrows():
                try:
                    if "client_email" not in frame.columns:
                        raise ValueError("missing column client_email")

                    email = row.get("client_email")
                    if pd.isna(email):
                        raise ValueError("client_email is required")

                    client_id = self._resolve_client_id(str(email))

                    values = {"client_id": client_id}

                    for column in repo.columns:
                        if column == "client_id":
                            continue

                        if column not in frame.columns:
                            raise ValueError(f"missing column {column}")

                        value = row[column]

                        if column == "recorded_on":
                            if pd.isna(value):
                                raise ValueError("recorded_on is required")
                            value = pd.to_datetime(value).date().isoformat()
                        elif pd.isna(value):
                            value = (
                                ""
                                if column in {"notes", "journal_entry"}
                                else None
                            )

                        values[column] = value

                    repo.create(values)
                    imported += 1

                except Exception as exc:
                    rejected += 1
                    errors.append(f"{sheet} row {index + 2}: {exc}")

        return ImportResult(imported, rejected, errors)
