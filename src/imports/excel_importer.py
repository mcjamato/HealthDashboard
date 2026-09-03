from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO

import pandas as pd

from configuration.intake_fields import (
    BOOLEAN_FIELDS,
    DATE_FIELDS,
    INTAKE_IMPORT_COLUMNS,
    INTAKE_KEYS,
    MULTISELECT_FIELDS,
    NUMERIC_FIELDS,
)
from repositories.client_repository import ClientRepository


@dataclass
class ImportResult:
    imported: int
    rejected: int
    errors: list[str]


class ExcelImporter:
    SHEETS = {"Clients", "Exercise", "Health", "MentalWellness", "Nutrition"}

    def __init__(
        self,
        clients,
        exercise,
        health,
        mental,
        nutrition,
        intake=None,
    ) -> None:
        """Create an importer with backward-compatible dependency ordering.

        Versions before 1.6.0 supplied the five core repositories after
        ``clients``. Version 1.6.0 added the intake repository. Keeping intake
        optional and last means an older app/importer combination cannot fail
        merely because the intake dependency was introduced.
        """
        self.clients: ClientRepository = clients
        self.intake = intake
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
            "Clients": INTAKE_IMPORT_COLUMNS,
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
                pd.DataFrame(columns=columns).to_excel(writer, sheet_name=name, index=False)
        return output.getvalue()

    def _resolve_client_id(self, email: str) -> int:
        client = self.clients.get_by_email(email)
        if client is None:
            raise ValueError(f"Unknown client_email: {email}")
        return int(client["id"])

    @staticmethod
    def _intake_values(row) -> dict:
        values = {}
        for key in INTAKE_KEYS:
            value = row.get(key)
            if pd.isna(value):
                value = None
            elif key in BOOLEAN_FIELDS:
                value = str(value).strip().lower() in {"1", "true", "yes", "y", "checked"}
            elif key in NUMERIC_FIELDS:
                value = float(value) if value is not None else None
                if value is not None and key in {"exercise_frequency_weekly", "stress_level", "readiness_score"}:
                    value = int(value)
            elif key in DATE_FIELDS:
                value = pd.to_datetime(value).date().isoformat() if value is not None else None
            elif key in MULTISELECT_FIELDS:
                value = str(value).strip() if value is not None else None
            else:
                value = str(value).strip() if value is not None else None
            values[key] = value
        return values


    def import_clients_csv(self, content: bytes) -> ImportResult:
        """Import client identity and full intake questionnaire from CSV."""
        try:
            frame = pd.read_csv(BytesIO(content))
        except Exception as exc:
            return ImportResult(0, 0, [f"Could not read CSV: {exc}"])

        imported = 0
        rejected = 0
        errors: list[str] = []

        for index, row in frame.iterrows():
            try:
                first = row.get("first_name")
                last = row.get("last_name")
                email = row.get("email")
                if pd.isna(first) or pd.isna(last) or pd.isna(email):
                    raise ValueError("first_name, last_name, and email are required")

                email_text = str(email).strip().lower()
                existing = self.clients.get_by_email(email_text)
                birth = row.get("birth_date")
                birth_text = None if pd.isna(birth) else pd.to_datetime(birth).date().isoformat()

                if existing is None:
                    client_id = self.clients.create(str(first), str(last), email_text, birth_text)
                else:
                    client_id = int(existing["id"])

                if self.intake is not None:
                    self.intake.upsert(client_id, self._intake_values(row))
                imported += 1
            except Exception as exc:
                rejected += 1
                errors.append(f"CSV row {index + 2}: {exc}")

        return ImportResult(imported, rejected, errors)

    def import_workbook(self, content: bytes) -> ImportResult:
        book = pd.ExcelFile(BytesIO(content))
        missing = self.SHEETS.difference(book.sheet_names)
        if missing:
            return ImportResult(0, 0, [f"Missing worksheets: {sorted(missing)}"])

        imported = 0
        rejected = 0
        errors: list[str] = []

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
                birth = row.get("birth_date")
                birth_text = None if pd.isna(birth) else pd.to_datetime(birth).date().isoformat()

                if existing is None:
                    client_id = self.clients.create(str(first), str(last), email_text, birth_text)
                else:
                    client_id = int(existing["id"])

                if self.intake is not None:
                    self.intake.upsert(client_id, self._intake_values(row))
                imported += 1
            except Exception as exc:
                rejected += 1
                errors.append(f"Clients row {index + 2}: {exc}")

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
                            value = "" if column in {"notes", "journal_entry"} else None
                        values[column] = value
                    repo.create(values)
                    imported += 1
                except Exception as exc:
                    rejected += 1
                    errors.append(f"{sheet} row {index + 2}: {exc}")

        return ImportResult(imported, rejected, errors)
