from __future__ import annotations

import math
from typing import Iterable

import pandas as pd


class AnalyticsService:
    """Provides reusable analytics calculations and display helpers."""

    @staticmethod
    def percent_change(values: Iterable[float]) -> float | None:
        """Calculate percent change between the last two chronological values."""
        clean_values = [
            float(value)
            for value in values
            if pd.notna(value)
        ]
        if len(clean_values) < 2:
            return None

        previous_value = clean_values[-2]
        current_value = clean_values[-1]

        if previous_value == 0:
            return None

        return ((current_value - previous_value) / abs(previous_value)) * 100

    @staticmethod
    def percent_change_for_frame(
        frame: pd.DataFrame,
        column: str,
    ) -> float | None:
        """Calculate percent change after sorting a frame by recorded date."""
        if frame.empty or column not in frame.columns:
            return None

        ordered = AnalyticsService.prepare_chronological(frame)
        values = pd.to_numeric(
            ordered[column],
            errors="coerce",
        ).dropna().tolist()

        return AnalyticsService.percent_change(values)

    @staticmethod
    def latest_value(
        frame: pd.DataFrame,
        column: str,
    ) -> float | None:
        """Return the latest valid numeric value."""
        if frame.empty or column not in frame.columns:
            return None

        ordered = frame.copy()
        if "recorded_on" in ordered.columns:
            ordered["recorded_on"] = pd.to_datetime(
                ordered["recorded_on"],
                errors="coerce",
            )
            ordered = ordered.sort_values(
                ["recorded_on", "id"],
                ascending=[False, False],
            )

        values = pd.to_numeric(
            ordered[column],
            errors="coerce",
        ).dropna()

        return None if values.empty else float(values.iloc[0])

    @staticmethod
    def mean(
        frame: pd.DataFrame,
        column: str,
    ) -> float | None:
        """Return the average numeric value."""
        if frame.empty or column not in frame.columns:
            return None

        value = pd.to_numeric(
            frame[column],
            errors="coerce",
        ).mean()

        return None if math.isnan(value) else float(value)

    @staticmethod
    def sum(
        frame: pd.DataFrame,
        column: str,
    ) -> float:
        """Return a numeric column total."""
        if frame.empty or column not in frame.columns:
            return 0.0

        return float(
            pd.to_numeric(
                frame[column],
                errors="coerce",
            ).fillna(0).sum()
        )

    @staticmethod
    def prepare_chronological(
        frame: pd.DataFrame,
    ) -> pd.DataFrame:
        """Convert dates and place records in chronological order."""
        if frame.empty:
            return frame.copy()

        result = frame.copy()
        result["recorded_on"] = pd.to_datetime(
            result["recorded_on"],
            errors="coerce",
        )

        sort_columns = ["recorded_on"]
        if "id" in result.columns:
            sort_columns.append("id")

        return result.sort_values(sort_columns)

    @staticmethod
    def format_change(change: float | None) -> str:
        """Format a percentage change for a Streamlit metric delta."""
        if change is None:
            return "Not enough data"
        return f"{change:+.1f}%"
