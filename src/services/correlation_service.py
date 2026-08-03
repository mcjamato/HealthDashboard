from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class CorrelationResult:
    metric_one: str
    metric_two: str
    coefficient: float
    sample_size: int
    strength: str
    direction: str


class CorrelationService:
    """Builds daily cross-domain data and calculates Pearson correlations."""

    METRIC_LABELS = {
        "exercise_minutes": "Exercise minutes",
        "calories_burned": "Calories burned",
        "steps": "Steps",
        "sleep_hours": "Sleep hours",
        "sleep_quality": "Sleep quality",
        "weight_kg": "Weight",
        "water_liters_health": "Health water",
        "mood_score": "Mood",
        "stress_score": "Stress",
        "energy_score": "Energy",
        "focus_score": "Focus",
        "meditation_minutes": "Meditation minutes",
        "nutrition_calories": "Nutrition calories",
        "protein_g": "Protein",
        "carbs_g": "Carbohydrates",
        "fat_g": "Fat",
        "fiber_g": "Fiber",
        "water_liters_nutrition": "Nutrition water",
    }

    @staticmethod
    def _daily_sum(
        frame: pd.DataFrame,
        mapping: dict[str, str],
    ) -> pd.DataFrame:
        if frame.empty:
            return pd.DataFrame(columns=["recorded_on", *mapping.values()])

        work = frame.copy()
        work["recorded_on"] = pd.to_datetime(
            work["recorded_on"],
            errors="coerce",
        ).dt.normalize()

        source_columns = list(mapping.keys())
        for column in source_columns:
            work[column] = pd.to_numeric(
                work[column],
                errors="coerce",
            )

        daily = (
            work.groupby("recorded_on", as_index=False)[source_columns]
            .sum(min_count=1)
            .rename(columns=mapping)
        )
        return daily

    @staticmethod
    def _daily_mean(
        frame: pd.DataFrame,
        mapping: dict[str, str],
    ) -> pd.DataFrame:
        if frame.empty:
            return pd.DataFrame(columns=["recorded_on", *mapping.values()])

        work = frame.copy()
        work["recorded_on"] = pd.to_datetime(
            work["recorded_on"],
            errors="coerce",
        ).dt.normalize()

        source_columns = list(mapping.keys())
        for column in source_columns:
            work[column] = pd.to_numeric(
                work[column],
                errors="coerce",
            )

        daily = (
            work.groupby("recorded_on", as_index=False)[source_columns]
            .mean()
            .rename(columns=mapping)
        )
        return daily

    def build_daily_dataset(
        self,
        exercise: pd.DataFrame,
        health: pd.DataFrame,
        mental: pd.DataFrame,
        nutrition: pd.DataFrame,
    ) -> pd.DataFrame:
        """Combine all four domains into one row per client date."""
        exercise_daily = self._daily_sum(
            exercise,
            {
                "duration_minutes": "exercise_minutes",
                "calories_burned": "calories_burned",
                "steps": "steps",
            },
        )

        health_daily = self._daily_mean(
            health,
            {
                "sleep_hours": "sleep_hours",
                "sleep_quality": "sleep_quality",
                "weight_kg": "weight_kg",
                "water_liters": "water_liters_health",
            },
        )

        mental_daily = self._daily_mean(
            mental,
            {
                "mood_score": "mood_score",
                "stress_score": "stress_score",
                "energy_score": "energy_score",
                "focus_score": "focus_score",
                "meditation_minutes": "meditation_minutes",
            },
        )

        nutrition_daily = self._daily_sum(
            nutrition,
            {
                "calories": "nutrition_calories",
                "protein_g": "protein_g",
                "carbs_g": "carbs_g",
                "fat_g": "fat_g",
                "fiber_g": "fiber_g",
                "water_liters": "water_liters_nutrition",
            },
        )

        frames = [
            exercise_daily,
            health_daily,
            mental_daily,
            nutrition_daily,
        ]

        combined: pd.DataFrame | None = None
        for frame in frames:
            if combined is None:
                combined = frame
            else:
                combined = combined.merge(
                    frame,
                    on="recorded_on",
                    how="outer",
                )

        if combined is None:
            return pd.DataFrame()

        return combined.sort_values("recorded_on").reset_index(drop=True)

    @staticmethod
    def correlation_matrix(
        daily_data: pd.DataFrame,
    ) -> pd.DataFrame:
        """Return a Pearson correlation matrix for numeric columns."""
        if daily_data.empty:
            return pd.DataFrame()

        numeric = daily_data.drop(
            columns=["recorded_on"],
            errors="ignore",
        ).apply(pd.to_numeric, errors="coerce")

        usable = numeric.loc[:, numeric.notna().sum() >= 2]
        if usable.shape[1] < 2:
            return pd.DataFrame()

        return usable.corr(method="pearson", min_periods=2)

    def strongest_relationships(
        self,
        matrix: pd.DataFrame,
        minimum_absolute: float = 0.30,
        limit: int = 8,
    ) -> list[CorrelationResult]:
        """Return strongest unique metric pairs from a matrix."""
        if matrix.empty:
            return []

        results: list[CorrelationResult] = []

        for row_index, first_metric in enumerate(matrix.columns):
            for second_metric in matrix.columns[row_index + 1:]:
                value = matrix.loc[first_metric, second_metric]
                if pd.isna(value) or abs(float(value)) < minimum_absolute:
                    continue

                coefficient = float(value)
                magnitude = abs(coefficient)

                if magnitude >= 0.70:
                    strength = "Strong"
                elif magnitude >= 0.50:
                    strength = "Moderate"
                else:
                    strength = "Weak"

                direction = "positive" if coefficient > 0 else "negative"

                results.append(
                    CorrelationResult(
                        metric_one=self.METRIC_LABELS.get(
                            first_metric, first_metric.replace("_", " ").title()
                        ),
                        metric_two=self.METRIC_LABELS.get(
                            second_metric, second_metric.replace("_", " ").title()
                        ),
                        coefficient=coefficient,
                        sample_size=0,
                        strength=strength,
                        direction=direction,
                    )
                )

        return sorted(
            results,
            key=lambda item: abs(item.coefficient),
            reverse=True,
        )[:limit]
