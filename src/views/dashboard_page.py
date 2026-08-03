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
from utilities.month_filter import MonthFilter


class DashboardPage:
    """Renders the main dashboard with monthly filtering."""

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
    def _sample_dates(
        days: int = 180,
    ) -> list[date]:
        """Return six months of sample dates ending today."""

        start = date.today() - timedelta(
            days=days - 1
        )

        return [
            start + timedelta(days=offset)
            for offset in range(days)
        ]

    def _sample_exercise(self) -> pd.DataFrame:
        """Create temporary exercise preview data."""

        dates = self._sample_dates()

        return pd.DataFrame(
            {
                "recorded_on": dates,
                "duration_minutes": [
                    25 + (index % 7) * 4
                    for index in range(len(dates))
                ],
                "calories_burned": [
                    170 + (index % 8) * 18
                    for index in range(len(dates))
                ],
            }
        )

    def _sample_health(self) -> pd.DataFrame:
        """Create temporary health preview data."""

        dates = self._sample_dates()

        return pd.DataFrame(
            {
                "recorded_on": dates,
                "sleep_hours": [
                    round(
                        6.7
                        + (index / len(dates)) * 0.9
                        + (index % 5) * 0.05,
                        1,
                    )
                    for index in range(len(dates))
                ],
                "sleep_quality": [
                    min(
                        10,
                        6 + index // 45,
                    )
                    for index in range(len(dates))
                ],
            }
        )

    def _sample_mental(self) -> pd.DataFrame:
        """Create temporary mental-wellness preview data."""

        dates = self._sample_dates()

        return pd.DataFrame(
            {
                "recorded_on": dates,
                "mood_score": [
                    min(
                        10,
                        5 + index // 40,
                    )
                    for index in range(len(dates))
                ],
                "stress_score": [
                    max(
                        2,
                        8 - index // 45,
                    )
                    for index in range(len(dates))
                ],
                "energy_score": [
                    min(
                        10,
                        5 + index // 45,
                    )
                    for index in range(len(dates))
                ],
            }
        )

    def _sample_nutrition(self) -> pd.DataFrame:
        """Create temporary nutrition preview data."""

        dates = self._sample_dates()

        return pd.DataFrame(
            {
                "recorded_on": dates,
                "calories": [
                    1950 + (index % 7) * 45
                    for index in range(len(dates))
                ],
                "protein_g": [
                    90 + (index % 6) * 4
                    for index in range(len(dates))
                ],
            }
        )

    @staticmethod
    def _style_figure(
        figure,
        sample: bool,
    ) -> None:
        """Apply shared Plotly formatting."""

        figure.update_layout(
            margin={
                "l": 20,
                "r": 20,
                "t": 65,
                "b": 20,
            },
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
                font={
                    "size": 11,
                },
            )

    @staticmethod
    def _combine_dates(
        *frames: pd.DataFrame,
    ) -> pd.DataFrame:
        """Combine recorded dates from all dashboard domains."""

        date_frames = [
            frame[["recorded_on"]]
            for frame in frames
            if (
                not frame.empty
                and "recorded_on" in frame.columns
            )
        ]

        if not date_frames:
            return pd.DataFrame(
                columns=["recorded_on"]
            )

        return pd.concat(
            date_frames,
            ignore_index=True,
        )

    def render(
        self,
        client_id: int | None,
    ) -> None:
        st.title("📊 Dashboard")

        st.caption(
            "Select a month to recalculate all "
            "dashboard metrics and charts."
        )

        if client_id is None:
            exercise = pd.DataFrame()
            health = pd.DataFrame()
            mental = pd.DataFrame()
            nutrition = pd.DataFrame()

            st.info(
                "No customer is selected. Sample data "
                "is displayed for interface preview."
            )
        else:
            exercise = (
                self.exercise_repository
                .list_for_client(client_id)
            )

            health = (
                self.health_repository
                .list_for_client(client_id)
            )

            mental = (
                self.mental_repository
                .list_for_client(client_id)
            )

            nutrition = (
                self.nutrition_repository
                .list_for_client(client_id)
            )

        exercise_is_sample = exercise.empty
        health_is_sample = health.empty
        mental_is_sample = mental.empty
        nutrition_is_sample = nutrition.empty

        display_exercise = (
            self._sample_exercise()
            if exercise_is_sample
            else exercise
        )

        display_health = (
            self._sample_health()
            if health_is_sample
            else health
        )

        display_mental = (
            self._sample_mental()
            if mental_is_sample
            else mental
        )

        display_nutrition = (
            self._sample_nutrition()
            if nutrition_is_sample
            else nutrition
        )

        st.subheader("Dashboard filters")

        available_dates = self._combine_dates(
            display_exercise,
            display_health,
            display_mental,
            display_nutrition,
        )

        selected_month = MonthFilter.select_month(
            frame=available_dates,
            key="main_dashboard_month",
            label="Display month",
        )

        display_exercise = MonthFilter.filter(
            display_exercise,
            selected_month,
        )

        display_health = MonthFilter.filter(
            display_health,
            selected_month,
        )

        display_mental = MonthFilter.filter(
            display_mental,
            selected_month,
        )

        display_nutrition = MonthFilter.filter(
            display_nutrition,
            selected_month,
        )

        st.caption(
            f"Showing: {selected_month}"
        )

        if any(
            frame.empty
            for frame in [
                display_exercise,
                display_health,
                display_mental,
                display_nutrition,
            ]
        ):
            st.warning(
                "One or more domains do not contain "
                "records for the selected month."
            )

        metric_columns = st.columns(4)

        exercise_minutes = (
            self.analytics.sum(
                display_exercise,
                "duration_minutes",
            )
        )

        exercise_change = (
            self.analytics
            .percent_change_for_frame(
                display_exercise,
                "duration_minutes",
            )
        )

        metric_columns[0].metric(
            "Exercise minutes",
            f"{exercise_minutes:.0f}",
            self.analytics.format_change(
                exercise_change
            ),
        )

        latest_sleep = (
            self.analytics.latest_value(
                display_health,
                "sleep_hours",
            )
            or 0
        )

        sleep_change = (
            self.analytics
            .percent_change_for_frame(
                display_health,
                "sleep_hours",
            )
        )

        metric_columns[1].metric(
            "Latest sleep",
            f"{latest_sleep:.1f} hr",
            self.analytics.format_change(
                sleep_change
            ),
        )

        latest_mood = (
            self.analytics.latest_value(
                display_mental,
                "mood_score",
            )
            or 0
        )

        mood_change = (
            self.analytics
            .percent_change_for_frame(
                display_mental,
                "mood_score",
            )
        )

        metric_columns[2].metric(
            "Latest mood",
            f"{latest_mood:.1f}/10",
            self.analytics.format_change(
                mood_change
            ),
        )

        recorded_calories = (
            self.analytics.sum(
                display_nutrition,
                "calories",
            )
        )

        calorie_change = (
            self.analytics
            .percent_change_for_frame(
                display_nutrition,
                "calories",
            )
        )

        metric_columns[3].metric(
            "Recorded calories",
            f"{recorded_calories:.0f}",
            self.analytics.format_change(
                calorie_change
            ),
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
                "One or more panels use sample data. "
                "Sample values are not written to SQLite."
            )

        st.divider()
        st.subheader("Domain trends")

        left, right = st.columns(2)

        if display_exercise.empty:
            left.info(
                "No exercise records are available "
                "for this month."
            )
        else:
            exercise_figure = px.line(
                display_exercise,
                x="recorded_on",
                y="duration_minutes",
                markers=True,
                title="Exercise duration",
                labels={
                    "recorded_on": "Date",
                    "duration_minutes": "Minutes",
                },
            )

            self._style_figure(
                exercise_figure,
                exercise_is_sample,
            )

            left.plotly_chart(
                exercise_figure,
                use_container_width=True,
            )

        if display_health.empty:
            right.info(
                "No health records are available "
                "for this month."
            )
        else:
            health_figure = px.line(
                display_health,
                x="recorded_on",
                y=[
                    "sleep_hours",
                    "sleep_quality",
                ],
                markers=True,
                title="Sleep duration and quality",
                labels={
                    "recorded_on": "Date",
                    "value": "Measurement",
                    "variable": "Metric",
                },
            )

            self._style_figure(
                health_figure,
                health_is_sample,
            )

            right.plotly_chart(
                health_figure,
                use_container_width=True,
            )

        left_two, right_two = st.columns(2)

        if display_mental.empty:
            left_two.info(
                "No mental-wellness records are "
                "available for this month."
            )
        else:
            mental_figure = px.line(
                display_mental,
                x="recorded_on",
                y=[
                    "mood_score",
                    "stress_score",
                    "energy_score",
                ],
                markers=True,
                title="Mood, stress, and energy",
                labels={
                    "recorded_on": "Date",
                    "value": "Score",
                    "variable": "Metric",
                },
            )

            mental_figure.update_yaxes(
                range=[0, 10]
            )

            self._style_figure(
                mental_figure,
                mental_is_sample,
            )

            left_two.plotly_chart(
                mental_figure,
                use_container_width=True,
            )

        if display_nutrition.empty:
            right_two.info(
                "No nutrition records are available "
                "for this month."
            )
        else:
            nutrition_figure = px.bar(
                display_nutrition,
                x="recorded_on",
                y="calories",
                title="Calories by date",
                labels={
                    "recorded_on": "Date",
                    "calories": "Calories",
                },
            )

            self._style_figure(
                nutrition_figure,
                nutrition_is_sample,
            )

            right_two.plotly_chart(
                nutrition_figure,
                use_container_width=True,
            )

        st.subheader(
            "Templates reserved for later versions"
        )

        goal_column, notification_column = (
            st.columns(2)
        )

        goal_column.info(
            "🎯 Goals\n\n"
            "Template placeholder — not active yet."
        )

        notification_column.info(
            "🔔 Notifications\n\n"
            "Template placeholder — not active yet."
        )
