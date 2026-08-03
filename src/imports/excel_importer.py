from dataclasses import dataclass
from io import BytesIO
import pandas as pd

@dataclass
class ImportResult:
    imported: int
    rejected: int
    errors: list[str]

class ExcelImporter:
    SHEETS = {"Clients", "Exercise", "Health", "MentalWellness", "Nutrition"}

    def __init__(self, clients, exercise, health, mental, nutrition):
        self.clients = clients
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
            "Clients": ["first_name", "last_name", "email", "birth_date"],
            "Exercise": ["client_id", "recorded_on", "exercise_type", "duration_minutes", "intensity", "steps", "distance_km", "calories_burned", "notes"],
            "Health": ["client_id", "recorded_on", "weight_kg", "sleep_hours", "sleep_quality", "resting_heart_rate", "systolic_bp", "diastolic_bp", "water_liters", "notes"],
            "MentalWellness": ["client_id", "recorded_on", "mood_score", "stress_score", "energy_score", "focus_score", "meditation_minutes", "journal_entry"],
            "Nutrition": ["client_id", "recorded_on", "meal_type", "calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "water_liters", "notes"],
        }
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            for name, columns in sheets.items():
                pd.DataFrame(columns=columns).to_excel(writer, sheet_name=name, index=False)
        return output.getvalue()

    def import_workbook(self, content: bytes) -> ImportResult:
        workbook = pd.ExcelFile(BytesIO(content))
        missing = self.SHEETS.difference(workbook.sheet_names)
        if missing:
            return ImportResult(0, 0, [f"Missing worksheets: {sorted(missing)}"])

        imported = rejected = 0
        errors: list[str] = []
        clients = pd.read_excel(workbook, sheet_name="Clients")
        for index, row in clients.iterrows():
            try:
                if pd.isna(row.get("first_name")) or pd.isna(row.get("last_name")):
                    raise ValueError("first and last name are required")
                birth = row.get("birth_date")
                self.clients.create(
                    str(row["first_name"]),
                    str(row["last_name"]),
                    "" if pd.isna(row.get("email")) else str(row.get("email")),
                    None if pd.isna(birth) else pd.to_datetime(birth).date().isoformat(),
                )
                imported += 1
            except Exception as exc:
                rejected += 1
                errors.append(f"Clients row {index + 2}: {exc}")

        for sheet, repo in self.repos.items():
            frame = pd.read_excel(workbook, sheet_name=sheet)
            for index, row in frame.iterrows():
                try:
                    values = {}
                    for column in repo.columns:
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
