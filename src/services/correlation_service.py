from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class CorrelationResult:
    metric_one: str
    metric_two: str
    coefficient: float
    strength: str
    direction: str


class CorrelationService:
    METRIC_LABELS = {
        "exercise_minutes": "Exercise minutes",
        "calories_burned": "Calories burned",
        "steps": "Steps",
        "sleep_hours": "Sleep hours",
        "sleep_quality": "Sleep quality",
        "weight_kg": "Weight",
        "mood_score": "Mood",
        "stress_score": "Stress",
        "energy_score": "Energy",
        "focus_score": "Focus",
        "nutrition_calories": "Nutrition calories",
        "protein_g": "Protein",
        "carbs_g": "Carbohydrates",
        "fat_g": "Fat",
        "fiber_g": "Fiber",
    }

    @staticmethod
    def _daily(frame: pd.DataFrame, mapping: dict[str, str], how: str) -> pd.DataFrame:
        if frame.empty:
            return pd.DataFrame(columns=["recorded_on", *mapping.values()])
        work = frame.copy()
        work["recorded_on"] = pd.to_datetime(
            work["recorded_on"], errors="coerce"
        ).dt.normalize()
        source = list(mapping.keys())
        for column in source:
            work[column] = pd.to_numeric(work[column], errors="coerce")
        grouped = work.groupby("recorded_on", as_index=False)[source]
        result = (
            grouped.sum(min_count=1)
            if how == "sum"
            else grouped.mean()
        )
        return result.rename(columns=mapping)

    def build_daily_dataset(
        self,
        exercise: pd.DataFrame,
        health: pd.DataFrame,
        mental: pd.DataFrame,
        nutrition: pd.DataFrame,
    ) -> pd.DataFrame:
        frames = [
            self._daily(
                exercise,
                {
                    "duration_minutes": "exercise_minutes",
                    "calories_burned": "calories_burned",
                    "steps": "steps",
                },
                "sum",
            ),
            self._daily(
                health,
                {
                    "sleep_hours": "sleep_hours",
                    "sleep_quality": "sleep_quality",
                    "weight_kg": "weight_kg",
                },
                "mean",
            ),
            self._daily(
                mental,
                {
                    "mood_score": "mood_score",
                    "stress_score": "stress_score",
                    "energy_score": "energy_score",
                    "focus_score": "focus_score",
                },
                "mean",
            ),
            self._daily(
                nutrition,
                {
                    "calories": "nutrition_calories",
                    "protein_g": "protein_g",
                    "carbs_g": "carbs_g",
                    "fat_g": "fat_g",
                    "fiber_g": "fiber_g",
                },
                "sum",
            ),
        ]

        combined = None
        for frame in frames:
            combined = frame if combined is None else combined.merge(
                frame, on="recorded_on", how="outer"
            )
        return (
            pd.DataFrame()
            if combined is None
            else combined.sort_values("recorded_on").reset_index(drop=True)
        )

    @staticmethod
    def correlation_matrix(daily_data: pd.DataFrame) -> pd.DataFrame:
        if daily_data.empty:
            return pd.DataFrame()
        numeric = daily_data.drop(
            columns=["recorded_on"], errors="ignore"
        ).apply(pd.to_numeric, errors="coerce")
        usable = numeric.loc[:, numeric.notna().sum() >= 2]
        return (
            pd.DataFrame()
            if usable.shape[1] < 2
            else usable.corr(method="pearson", min_periods=2)
        )
