from __future__ import annotations

import math
from typing import Iterable

import pandas as pd


class AnalyticsService:
    @staticmethod
    def percent_change(values: Iterable[float]) -> float | None:
        clean = [float(value) for value in values if pd.notna(value)]
        if len(clean) < 2 or clean[-2] == 0:
            return None
        return ((clean[-1] - clean[-2]) / abs(clean[-2])) * 100

    @staticmethod
    def percent_change_for_frame(frame: pd.DataFrame, column: str) -> float | None:
        if frame.empty or column not in frame.columns:
            return None
        ordered = AnalyticsService.prepare_chronological(frame)
        values = pd.to_numeric(
            ordered[column], errors="coerce"
        ).dropna().tolist()
        return AnalyticsService.percent_change(values)

    @staticmethod
    def latest_value(frame: pd.DataFrame, column: str) -> float | None:
        if frame.empty or column not in frame.columns:
            return None
        ordered = frame.copy()
        ordered["recorded_on"] = pd.to_datetime(
            ordered["recorded_on"], errors="coerce"
        )
        sort_columns = ["recorded_on"]
        ascending = [False]
        if "id" in ordered.columns:
            sort_columns.append("id")
            ascending.append(False)
        ordered = ordered.sort_values(sort_columns, ascending=ascending)
        values = pd.to_numeric(
            ordered[column], errors="coerce"
        ).dropna()
        return None if values.empty else float(values.iloc[0])

    @staticmethod
    def mean(frame: pd.DataFrame, column: str) -> float | None:
        if frame.empty or column not in frame.columns:
            return None
        value = pd.to_numeric(frame[column], errors="coerce").mean()
        return None if math.isnan(value) else float(value)

    @staticmethod
    def sum(frame: pd.DataFrame, column: str) -> float:
        if frame.empty or column not in frame.columns:
            return 0.0
        return float(
            pd.to_numeric(frame[column], errors="coerce").fillna(0).sum()
        )

    @staticmethod
    def prepare_chronological(frame: pd.DataFrame) -> pd.DataFrame:
        if frame.empty:
            return frame.copy()
        result = frame.copy()
        result["recorded_on"] = pd.to_datetime(
            result["recorded_on"], errors="coerce"
        )
        sort_columns = ["recorded_on"]
        if "id" in result.columns:
            sort_columns.append("id")
        return result.sort_values(sort_columns)

    @staticmethod
    def format_change(change: float | None) -> str:
        return "Not enough data" if change is None else f"{change:+.1f}%"
