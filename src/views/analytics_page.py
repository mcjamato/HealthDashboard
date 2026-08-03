from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from repositories.domain_repository import (
    ExerciseRepository,
    HealthRepository,
    MentalWellnessRepository,
    NutritionRepository,
)
from services.correlation_service import CorrelationService


class AnalyticsPage:
    """Renders cross-domain correlation analysis."""

    def __init__(
        self,
        exercise_repository: ExerciseRepository,
        health_repository: HealthRepository,
        mental_repository: MentalWellnessRepository,
        nutrition_repository: NutritionRepository,
    ) -> None:
        self.exercise_repository = exercise_repository
        self.health_repository = health_repository
        self.mental_repository = mental_repository
        self.nutrition_repository = nutrition_repository
        self.correlations = CorrelationService()

    def render(self, client_id: int | None) -> None:
        st.title("🔗 Cross-Domain Analytics")
        st.caption(
            "Pearson correlation explores how metrics move together. "
            "Correlation does not prove causation."
        )

        if client_id is None:
            st.info("Create or select a client before running correlations.")
            return

        exercise = self.exercise_repository.list_for_client(client_id)
        health = self.health_repository.list_for_client(client_id)
        mental = self.mental_repository.list_for_client(client_id)
        nutrition = self.nutrition_repository.list_for_client(client_id)

        daily = self.correlations.build_daily_dataset(
            exercise,
            health,
            mental,
            nutrition,
        )

        if daily.empty or len(daily) < 2:
            st.warning(
                "Enter records on at least two dates before running cross-domain analytics."
            )
            return

        st.subheader("Combined daily dataset")
        display_daily = daily.copy()
        display_daily["recorded_on"] = pd.to_datetime(
            display_daily["recorded_on"]
        ).dt.date
        st.dataframe(
            display_daily,
            use_container_width=True,
            hide_index=True,
        )

        matrix = self.correlations.correlation_matrix(daily)
        if matrix.empty:
            st.warning(
                "More repeated numeric measurements are needed to calculate a matrix."
            )
            return

        st.subheader("Correlation matrix")
        st.plotly_chart(
            px.imshow(
                matrix,
                text_auto=".2f",
                zmin=-1,
                zmax=1,
                aspect="auto",
                title="Pearson correlation matrix",
            ),
            use_container_width=True,
        )

        st.subheader("Strongest relationships")
        relationships = self.correlations.strongest_relationships(matrix)

        if not relationships:
            st.info("No relationships met the current 0.30 strength threshold.")
        else:
            relationship_rows = [
                {
                    "Metric one": result.metric_one,
                    "Metric two": result.metric_two,
                    "Correlation": round(result.coefficient, 3),
                    "Strength": result.strength,
                    "Direction": result.direction,
                }
                for result in relationships
            ]
            st.dataframe(
                pd.DataFrame(relationship_rows),
                use_container_width=True,
                hide_index=True,
            )

            for result in relationships[:3]:
                st.info(
                    f"{result.strength} {result.direction} relationship: "
                    f"{result.metric_one} and {result.metric_two} "
                    f"(r = {result.coefficient:.2f})."
                )

        st.subheader("Explore two metrics")
        metric_options = [
            column
            for column in matrix.columns
            if column in daily.columns
        ]

        if len(metric_options) >= 2:
            first_metric = st.selectbox(
                "First metric",
                metric_options,
                format_func=lambda name: self.correlations.METRIC_LABELS.get(
                    name, name.replace("_", " ").title()
                ),
            )
            remaining = [
                name for name in metric_options if name != first_metric
            ]
            second_metric = st.selectbox(
                "Second metric",
                remaining,
                format_func=lambda name: self.correlations.METRIC_LABELS.get(
                    name, name.replace("_", " ").title()
                ),
            )

            scatter_data = daily[
                ["recorded_on", first_metric, second_metric]
            ].dropna()

            if len(scatter_data) >= 2:
                st.plotly_chart(
                    px.scatter(
                        scatter_data,
                        x=first_metric,
                        y=second_metric,
                        hover_data=["recorded_on"],
                        trendline="ols" if len(scatter_data) >= 3 else None,
                        title=(
                            f"{self.correlations.METRIC_LABELS.get(first_metric, first_metric)} "
                            f"vs. {self.correlations.METRIC_LABELS.get(second_metric, second_metric)}"
                        ),
                    ),
                    use_container_width=True,
                )
            else:
                st.info("The selected pair needs at least two matching dates.")
