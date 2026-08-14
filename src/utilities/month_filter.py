from __future__ import annotations

import pandas as pd
import streamlit as st


class MonthFilter:
    ALL_MONTHS = "All months"

    @staticmethod
    def prepare(frame: pd.DataFrame) -> pd.DataFrame:
        if frame.empty:
            return frame.copy()
        if "recorded_on" not in frame.columns:
            raise ValueError("MonthFilter requires a 'recorded_on' column.")
        result = frame.copy()
        result["recorded_on"] = pd.to_datetime(
            result["recorded_on"], errors="coerce"
        )
        return result.dropna(subset=["recorded_on"])

    @staticmethod
    def available_months(frame: pd.DataFrame) -> list[str]:
        prepared = MonthFilter.prepare(frame)
        if prepared.empty:
            return []
        periods = prepared["recorded_on"].dt.to_period("M").dropna().unique()
        return [
            period.strftime("%B %Y")
            for period in sorted(periods, reverse=True)
        ]

    @staticmethod
    def select_month(frame: pd.DataFrame, key: str, label: str = "Display month") -> str:
        return st.selectbox(
            label,
            [MonthFilter.ALL_MONTHS, *MonthFilter.available_months(frame)],
            key=key,
        )

    @staticmethod
    def filter(frame: pd.DataFrame, selected_month: str) -> pd.DataFrame:
        prepared = MonthFilter.prepare(frame)
        if prepared.empty or selected_month == MonthFilter.ALL_MONTHS:
            return prepared
        labels = prepared["recorded_on"].dt.strftime("%B %Y")
        return prepared[labels == selected_month].copy()
