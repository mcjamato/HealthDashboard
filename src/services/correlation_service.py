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
    """Builds aligned daily data and pairwise Pearson correlations."""

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
    def _daily(
        frame: pd.DataFrame,
        mapping: dict[str, str],
        how: str,
    ) -> pd.DataFrame:
        if frame.empty:
            return pd.DataFrame(
                columns=[
                    "recorded_on",
                    *mapping.values(),
                ]
            )

        work = frame.copy()

        work["recorded_on"] = pd.to_datetime(
            work["recorded_on"],
            errors="coerce",
        ).dt.normalize()

        source = list(
            mapping.keys()
        )

        # Older or partial data sets may not contain every optional field.
        available_source = [
            column
            for column in source
            if column in work.columns
        ]

        if not available_source:
            return pd.DataFrame(
                columns=[
                    "recorded_on",
                    *mapping.values(),
                ]
            )

        work = work[
            [
                "recorded_on",
                *available_source,
            ]
        ].copy()

        for column in available_source:
            work[
                column
            ] = pd.to_numeric(
                work[column],
                errors="coerce",
            )

        grouped = work.groupby(
            "recorded_on",
            as_index=False,
        )[
            available_source
        ]

        result = (
            grouped.sum(
                min_count=1
            )
            if how == "sum"
            else grouped.mean()
        )

        return result.rename(
            columns={
                column: mapping[
                    column
                ]
                for column in available_source
            }
        )

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
            if frame.empty and len(
                frame.columns
            ) <= 1:
                continue

            combined = (
                frame
                if combined is None
                else combined.merge(
                    frame,
                    on="recorded_on",
                    how="outer",
                )
            )

        if combined is None:
            return pd.DataFrame()

        return (
            combined.sort_values(
                "recorded_on"
            )
            .reset_index(
                drop=True
            )
        )

    @staticmethod
    def available_metrics(
        daily_data: pd.DataFrame,
    ) -> list[str]:
        """Return numeric metrics with at least two usable observations."""

        if daily_data.empty:
            return []

        metrics: list[str] = []

        for column in daily_data.columns:
            if column == "recorded_on":
                continue

            values = pd.to_numeric(
                daily_data[column],
                errors="coerce",
            )

            if values.notna().sum() >= 2:
                metrics.append(
                    column
                )

        return metrics

    @staticmethod
    def pair_data(
        daily_data: pd.DataFrame,
        metric_one: str,
        metric_two: str,
    ) -> pd.DataFrame:
        """Return rows where both selected metrics have usable values."""

        required = [
            "recorded_on",
            metric_one,
            metric_two,
        ]

        if any(
            column not in daily_data.columns
            for column in required
        ):
            return pd.DataFrame(
                columns=required
            )

        result = daily_data[
            required
        ].copy()

        result[
            metric_one
        ] = pd.to_numeric(
            result[
                metric_one
            ],
            errors="coerce",
        )

        result[
            metric_two
        ] = pd.to_numeric(
            result[
                metric_two
            ],
            errors="coerce",
        )

        return result.dropna(
            subset=[
                metric_one,
                metric_two,
            ]
        )

    @staticmethod
    def describe_coefficient(
        coefficient: float,
    ) -> tuple[str, str]:
        absolute = abs(
            coefficient
        )

        if absolute >= 0.8:
            strength = "Very strong"
        elif absolute >= 0.6:
            strength = "Strong"
        elif absolute >= 0.4:
            strength = "Moderate"
        elif absolute >= 0.2:
            strength = "Weak"
        else:
            strength = "Very weak"

        if coefficient > 0:
            direction = "Positive"
        elif coefficient < 0:
            direction = "Negative"
        else:
            direction = "None"

        return (
            strength,
            direction,
        )

    def correlate(
        self,
        daily_data: pd.DataFrame,
        metric_one: str,
        metric_two: str,
    ) -> CorrelationResult | None:
        pair = self.pair_data(
            daily_data,
            metric_one,
            metric_two,
        )

        if len(
            pair
        ) < 2:
            return None

        coefficient = float(
            pair[
                [
                    metric_one,
                    metric_two,
                ]
            ].corr(
                method="pearson"
            ).iloc[
                0,
                1
            ]
        )

        if pd.isna(
            coefficient
        ):
            return None

        strength, direction = (
            self.describe_coefficient(
                coefficient
            )
        )

        return CorrelationResult(
            metric_one=metric_one,
            metric_two=metric_two,
            coefficient=coefficient,
            strength=strength,
            direction=direction,
        )

    @staticmethod
    def correlation_matrix(
        daily_data: pd.DataFrame,
    ) -> pd.DataFrame:
        if daily_data.empty:
            return pd.DataFrame()

        numeric = daily_data.drop(
            columns=[
                "recorded_on"
            ],
            errors="ignore",
        ).apply(
            pd.to_numeric,
            errors="coerce",
        )

        usable = numeric.loc[
            :,
            numeric.notna().sum()
            >= 2,
        ]

        if usable.shape[
            1
        ] < 2:
            return pd.DataFrame()

        return usable.corr(
            method="pearson",
            min_periods=2,
        )
