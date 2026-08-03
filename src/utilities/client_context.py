from __future__ import annotations

from datetime import date, datetime
from typing import Any

import pandas as pd


class ClientContext:
    """Builds safe display information for the selected client."""

    @staticmethod
    def calculate_age(
        birth_date: str | date | datetime | None,
    ) -> int | None:
        """Return age in completed years, or None when unavailable."""

        if birth_date is None or pd.isna(birth_date):
            return None

        try:
            parsed = pd.to_datetime(
                birth_date,
                errors="raise",
            ).date()
        except (TypeError, ValueError):
            return None

        today = date.today()

        return (
            today.year
            - parsed.year
            - (
                (today.month, today.day)
                < (parsed.month, parsed.day)
            )
        )

    @staticmethod
    def from_row(
        row: dict[str, Any] | None,
    ) -> dict[str, Any] | None:
        """Convert a client database row into display-ready context."""

        if not row:
            return None

        first_name = str(
            row.get("first_name", "")
        ).strip()

        last_name = str(
            row.get("last_name", "")
        ).strip()

        full_name = (
            f"{first_name} {last_name}"
        ).strip()

        email = row.get("email")
        birth_date = row.get("birth_date")

        return {
            "id": int(row["id"]),
            "full_name": full_name or "Unnamed client",
            "email": (
                str(email)
                if email and not pd.isna(email)
                else "Not provided"
            ),
            "birth_date": (
                str(birth_date)
                if birth_date and not pd.isna(birth_date)
                else "Not provided"
            ),
            "age": ClientContext.calculate_age(
                birth_date
            ),
        }
