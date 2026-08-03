from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
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
    """Renders the client dashboard with real data or labeled sample charts."""

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

    @staticmethod
    def _sample_dates(days: int = 7) -> list[date]:
        """Return a stable seven-day sample range ending today."""
        start = date.today() - timedelta(days=days - 1)
        return [start + timedelta(days=offset) for offset in range(days)]

    def _sample_exercise(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "recorded_on": self._sample_dates(),
                "duration_minutes": [20, 35, 25, 45, 30, 50, 40],
                "calories_burned": [120, 220, 155, 310, 190, 360, 275],
            }
        )

    def _sample_health(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "recorded_on": self._sample_dates(),
                "sleep_hours": [6.8, 7.2, 7.0, 7.7, 7.4, 8.0, 7.8],
                "sleep_quality": [6, 7, 7, 8, 7, 9, 8],
            }
        )

    def _sample_mental(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "recorded_on": self._sample_dates(),
                "mood_score": [6, 7, 6, 8, 7, 9, 8],
                "stress_score": [7, 6, 6, 5, 5, 4, 4],
                "energy_score": [5, 6, 6, 7, 7, 8, 8],
            }
        )

    def _sample_nutrition(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "recorded_on": self._sample_dates(),
                "calories": [2050, 1980, 2150, 2020, 2080, 2200, 2100],
                "protein_g": [95, 105, 100, 115, 110, 120, 118],
            }
        )

    @staticmethod
    def _style_figure(figure, sample: bool) -> None:
        """Apply consistent dashboard styling and sample-data labeling."""
        figure.update_layout(
            margin=dict(l=20, r=20, t=65, b=20),
            legend_title_text="",
        )
        if sample:
            figure.add_annotation(
                text="SAMPLE DATA",
                xref="paper",
                yref="paper",
                x=1,
                y=1.14,
                showarrow=False,
                font=dict(size=11),
            )

    def render(self, client_id: int | None) -> None:
        st.title("📊 Analytics Dashboard")
        st.caption(
            "Live client analytics are shown when records exist. "
            "Clearly labeled sample charts remain visible during setup."
        )

        if client_id is None:
            exercise = pd.DataFrame()
            health = pd.DataFrame()
            mental = pd.DataFrame()
            nutrition = pd.DataFrame()
            st.info(
                "No client is selected yet. The dashboard below uses sample data "
                "so you can preview the completed interface."
            )
        else:
            exercise = self.exercise_repository.list_for_client(client_id)
            health = self.health_repository.list_for_client(client_id)
            mental = self.mental_repository.list_for_client(client_id)
            nutrition = self.nutrition_repository.list_for_client(client_id)

        exercise_is_sample = exercise.empty
        health_is_sample = health.empty
        mental_is_sample = mental.empty
        nutrition_is_sample = nutrition.empty

        display_exercise = self._sample_exercise() if exercise_is_sample else exercise
        display_health = self._sample_health() if health_is_sample else health
        display_mental = self._sample_mental() if mental_is_sample else mental
        display_nutrition = self._sample_nutrition() if nutrition_is_sample else nutrition

        metric_columns = st.columns(4)

        if exercise_is_sample:
            exercise_minutes = float(display_exercise["duration_minutes"].sum())
            exercise_change = self.analytics.percent_change(
                display_exercise["duration_minutes"].tolist()
            )
        else:
            exercise_minutes = self.analytics.sum(exercise, "duration_minutes")
            exercise_change = self.analytics.percent_change_for_frame(
                exercise, "duration_minutes"
            )

        metric_columns[0].metric(
            "Exercise minutes",
            f"{exercise_minutes:.0f}",
            self.analytics.format_change(exercise_change),
        )

        if health_is_sample:
            latest_sleep = float(display_health["sleep_hours"].iloc[-1])
            sleep_change = self.analytics.percent_change(
                display_health["sleep_hours"].tolist()
            )
        else:
            latest_sleep = self.analytics.latest_value(health, "sleep_hours") or 0
            sleep_change = self.analytics.percent_change_for_frame(
                health, "sleep_hours"
            )

        metric_columns[1].metric(
            "Latest sleep",
            f"{latest_sleep:.1f} hr",
            self.analytics.format_change(sleep_change),
        )

        if mental_is_sample:
            latest_mood = float(display_mental["mood_score"].iloc[-1])
            mood_change = self.analytics.percent_change(
                display_mental["mood_score"].tolist()
            )
        else:
            latest_mood = self.analytics.latest_value(mental, "mood_score") or 0
            mood_change = self.analytics.percent_change_for_frame(
                mental, "mood_score"
            )

        metric_columns[2].metric(
            "Latest mood",
            f"{latest_mood:.1f}/10",
            self.analytics.format_change(mood_change),
        )

        if nutrition_is_sample:
            recorded_calories = float(display_nutrition["calories"].sum())
            calorie_change = self.analytics.percent_change(
                display_nutrition["calories"].tolist()
            )
        else:
            recorded_calories = self.analytics.sum(nutrition, "calories")
            calorie_change = self.analytics.percent_change_for_frame(
                nutrition, "calories"
            )

        metric_columns[3].metric(
            "Recorded calories",
            f"{recorded_calories:.0f}",
            self.analytics.format_change(calorie_change),
        )

        if any(
            [
                exercise_is_sample,
                health_is_sample,
                mental_is_sample,
                nutrition_is_sample,
            ]
        ):
            st.warning(
                "One or more panels use sample data. Sample values are never "
                "written to SQLite and disappear automatically when real records exist."
            )

        st.divider()
        st.subheader("Domain trends")

        left, right = st.columns(2)

        exercise_chart_data = self.analytics.prepare_chronological(display_exercise)
        exercise_figure = px.line(
            exercise_chart_data,
            x="recorded_on",
            y="duration_minutes",
            markers=True,
            title="Exercise duration",
            labels={"recorded_on": "Date", "duration_minutes": "Minutes"},
        )
        self._style_figure(exercise_figure, exercise_is_sample)
        left.plotly_chart(exercise_figure, use_container_width=True)

        health_chart_data = self.analytics.prepare_chronological(display_health)
        health_figure = px.line(
            health_chart_data,
            x="recorded_on",
            y=["sleep_hours", "sleep_quality"],
            markers=True,
            title="Sleep duration and quality",
            labels={"recorded_on": "Date", "value": "Measurement", "variable": "Metric"},
        )
        self._style_figure(health_figure, health_is_sample)
        right.plotly_chart(health_figure, use_container_width=True)

        left_two, right_two = st.columns(2)

        mental_chart_data = self.analytics.prepare_chronological(display_mental)
        mental_figure = px.line(
            mental_chart_data,
            x="recorded_on",
            y=["mood_score", "stress_score", "energy_score"],
            markers=True,
            title="Mood, stress, and energy",
            labels={"recorded_on": "Date", "value": "Score", "variable": "Metric"},
        )
        mental_figure.update_yaxes(range=[0, 10])
        self._style_figure(mental_figure, mental_is_sample)
        left_two.plotly_chart(mental_figure, use_container_width=True)

        nutrition_chart_data = self.analytics.prepare_chronological(display_nutrition)
        nutrition_figure = px.bar(
            nutrition_chart_data,
            x="recorded_on",
            y="calories",
            title="Calories by date",
            labels={"recorded_on": "Date", "calories": "Calories"},
        )
        self._style_figure(nutrition_figure, nutrition_is_sample)
        right_two.plotly_chart(nutrition_figure, use_container_width=True)

        st.subheader("Templates reserved for later versions")
        goal_column, notification_column = st.columns(2)
        goal_column.info("🎯 Goals\n\nTemplate placeholder — not active yet.")
        notification_column.info(
            "🔔 Notifications\n\nTemplate placeholder — not active yet."
        )
