from __future__ import annotations

import pandas as pd
import streamlit as st


class MonthFilter:
    """Provides reusable month filtering for dashboard DataFrames."""

    ALL_MONTHS = "All months"

    @staticmethod
    def prepare(frame: pd.DataFrame) -> pd.DataFrame:
        """Return a copy with recorded_on converted to pandas datetime."""
        if frame.empty:
            return frame.copy()

        if "recorded_on" not in frame.columns:
            raise ValueError(
                "MonthFilter requires a 'recorded_on' column."
            )

        prepared = frame.copy()
        prepared["recorded_on"] = pd.to_datetime(
            prepared["recorded_on"],
            errors="coerce",
        )

        return prepared.dropna(subset=["recorded_on"])

    @staticmethod
    def available_months(frame: pd.DataFrame) -> list[str]:
        """Return available months from newest to oldest."""
        prepared = MonthFilter.prepare(frame)

        if prepared.empty:
            return []

        periods = (
            prepared["recorded_on"]
            .dt.to_period("M")
            .dropna()
            .unique()
        )

        return [
            period.strftime("%B %Y")
            for period in sorted(periods, reverse=True)
        ]

    @staticmethod
    def select_month(
        frame: pd.DataFrame,
        key: str,
        label: str = "Display month",
    ) -> str:
        """Render a Streamlit selector and return the selected month."""
        options = [
            MonthFilter.ALL_MONTHS,
            *MonthFilter.available_months(frame),
        ]

        return st.selectbox(
            label,
            options,
            key=key,
        )

    @staticmethod
    def filter(
        frame: pd.DataFrame,
        selected_month: str,
    ) -> pd.DataFrame:
        """Filter a DataFrame to the selected Month Year."""
        prepared = MonthFilter.prepare(frame)

        if (
            prepared.empty
            or selected_month == MonthFilter.ALL_MONTHS
        ):
            return prepared

        month_labels = (
            prepared["recorded_on"]
            .dt.strftime("%B %Y")
        )

        return prepared[
            month_labels == selected_month
        ].copy()

    @staticmethod
    def apply(
        frame: pd.DataFrame,
        key: str,
        label: str = "Display month",
    ) -> tuple[pd.DataFrame, str]:
        """Render a selector and return the filtered frame and selection."""
        selected_month = MonthFilter.select_month(
            frame=frame,
            key=key,
            label=label,
        )

        filtered = MonthFilter.filter(
            frame=frame,
            selected_month=selected_month,
        )

        return filtered, selected_month
