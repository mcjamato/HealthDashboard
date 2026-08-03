from __future__ import annotations

import plotly.express as px
import streamlit as st

from repositories.domain_repository import (
    ExerciseRepository,
    HealthRepository,
    MentalWellnessRepository,
    NutritionRepository,
)
from services.analytics_service import AnalyticsService


class DashboardPage:
    """Renders the client-level Phase 3 analytics dashboard."""

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
        self.analytics = AnalyticsService()

    def render(self, client_id: int | None) -> None:
        st.title("📊 Analytics Dashboard")
        st.caption("Phase 3 summary metrics and trends across all four domains.")

        if client_id is None:
            st.info("Create or select a client to view analytics.")
            return

        exercise = self.exercise_repository.list_for_client(client_id)
        health = self.health_repository.list_for_client(client_id)
        mental = self.mental_repository.list_for_client(client_id)
        nutrition = self.nutrition_repository.list_for_client(client_id)

        row_one = st.columns(4)

        exercise_minutes = self.analytics.sum(
            exercise,
            "duration_minutes",
        )
        exercise_change = self.analytics.percent_change_for_frame(
            exercise,
            "duration_minutes",
        )
        row_one[0].metric(
            "Exercise minutes",
            f"{exercise_minutes:.0f}",
            self.analytics.format_change(exercise_change),
        )

        latest_sleep = self.analytics.latest_value(
            health,
            "sleep_hours",
        ) or 0
        sleep_change = self.analytics.percent_change_for_frame(
            health,
            "sleep_hours",
        )
        row_one[1].metric(
            "Latest sleep",
            f"{latest_sleep:.1f} hr",
            self.analytics.format_change(sleep_change),
        )

        latest_mood = self.analytics.latest_value(
            mental,
            "mood_score",
        ) or 0
        mood_change = self.analytics.percent_change_for_frame(
            mental,
            "mood_score",
        )
        row_one[2].metric(
            "Latest mood",
            f"{latest_mood:.1f}/10",
            self.analytics.format_change(mood_change),
        )

        nutrition_calories = self.analytics.sum(
            nutrition,
            "calories",
        )
        calories_change = self.analytics.percent_change_for_frame(
            nutrition,
            "calories",
        )
        row_one[3].metric(
            "Recorded calories",
            f"{nutrition_calories:.0f}",
            self.analytics.format_change(calories_change),
        )

        st.divider()
        st.subheader("Domain trends")

        left, right = st.columns(2)

        if not exercise.empty:
            exercise_chart = self.analytics.prepare_chronological(exercise)
            left.plotly_chart(
                px.line(
                    exercise_chart,
                    x="recorded_on",
                    y="duration_minutes",
                    markers=True,
                    title="Exercise duration",
                ),
                use_container_width=True,
            )
        else:
            left.info("Add exercise records to display this trend.")

        if not health.empty:
            health_chart = self.analytics.prepare_chronological(health)
            right.plotly_chart(
                px.line(
                    health_chart,
                    x="recorded_on",
                    y="sleep_hours",
                    markers=True,
                    title="Sleep hours",
                ),
                use_container_width=True,
            )
        else:
            right.info("Add health records to display this trend.")

        left_two, right_two = st.columns(2)

        if not mental.empty:
            mental_chart = self.analytics.prepare_chronological(mental)
            left_two.plotly_chart(
                px.line(
                    mental_chart,
                    x="recorded_on",
                    y=["mood_score", "stress_score", "energy_score"],
                    markers=True,
                    title="Mood, stress, and energy",
                ),
                use_container_width=True,
            )
        else:
            left_two.info("Add mental wellness records to display this trend.")

        if not nutrition.empty:
            nutrition_chart = self.analytics.prepare_chronological(nutrition)
            right_two.plotly_chart(
                px.bar(
                    nutrition_chart,
                    x="recorded_on",
                    y="calories",
                    title="Calories by entry date",
                ),
                use_container_width=True,
            )
        else:
            right_two.info("Add nutrition records to display this trend.")

        st.subheader("Templates reserved for later phases")
        template_one, template_two = st.columns(2)
        template_one.info("🎯 Goals\n\nTemplate placeholder - not active yet.")
        template_two.info("🔔 Notifications\n\nTemplate placeholder - not active yet.")
