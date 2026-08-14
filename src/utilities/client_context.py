from __future__ import annotations

from datetime import date

import pandas as pd


class ClientContext:
    @staticmethod
    def calculate_age(birth_date) -> int | None:
        if birth_date is None or pd.isna(birth_date):
            return None
        try:
            parsed = pd.to_datetime(birth_date, errors="raise").date()
        except (TypeError, ValueError):
            return None
        today = date.today()
        return (
            today.year
            - parsed.year
            - ((today.month, today.day) < (parsed.month, parsed.day))
        )

    @staticmethod
    def from_row(row: dict | None) -> dict | None:
        if not row:
            return None
        first = str(row.get("first_name", "")).strip()
        last = str(row.get("last_name", "")).strip()
        return {
            "id": int(row["id"]),
            "full_name": f"{first} {last}".strip() or "Unnamed client",
            "email": (
                str(row.get("email"))
                if row.get("email") and not pd.isna(row.get("email"))
                else "Not provided"
            ),
            "birth_date": (
                str(row.get("birth_date"))
                if row.get("birth_date") and not pd.isna(row.get("birth_date"))
                else "Not provided"
            ),
            "age": ClientContext.calculate_age(row.get("birth_date")),
        }
