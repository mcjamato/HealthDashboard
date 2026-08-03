from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

from components.layout import DashboardLayout
from repositories.domain_repository import (
    ExerciseRepository,
    HealthRepository,
    MentalWellnessRepository,
    NutritionRepository,
)
from services.analytics_service import AnalyticsService
from utilities.month_filter import MonthFilter


PLOTLY_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "responsive": True,
    "modeBarButtonsToRemove": [
        "lasso2d",
        "select2d",
    ],
}


class DashboardPage:
    """Renders the main dashboard using reusable layout components."""

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
        start = date.today() - timedelta(
            days=days - 1
        )

        return [
            start + timedelta(days=offset)
            for offset in range(days)
        ]

    def _sample_exercise(self) -> pd.DataFrame:
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
    def _combine_dates(
        *frames: pd.DataFrame,
    ) -> pd.DataFrame:
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

    @staticmethod
    def _style_figure(
        figure,
        sample: bool,
    ) -> None:
        figure.update_layout(
            margin={
                "l": 20,
                "r": 20,
                "t": 35,
                "b": 20,
            },
            legend_title_text="",
            hovermode="x unified",
        )

        if sample:
            figure.add_annotation(
                text="SAMPLE DATA",
                xref="paper",
                yref="paper",
                x=1,
                y=1.10,
                showarrow=False,
                font={
                    "size": 11,
                },
            )

    def render(
        self,
        client_id: int | None,
        client: dict | None = None,
    ) -> None:
        DashboardLayout.render_client_header(
            client=client,
            page_label="📊 Dashboard",
        )

        st.caption(
            "Select a month to recalculate all "
            "dashboard metrics and charts."
        )

        if client_id is None:
            exercise = pd.DataFrame()
            health = pd.DataFrame()
            mental = pd.DataFrame()
            nutrition = pd.DataFrame()
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

        available_dates = self._combine_dates(
            display_exercise,
            display_health,
            display_mental,
            display_nutrition,
        )

        selected_month = (
            DashboardLayout.render_filter_bar(
                render_filter=lambda: (
                    MonthFilter.select_month(
                        frame=available_dates,
                        key="main_dashboard_month",
                        label="Display month",
                    )
                ),
                title="Dashboard filters",
                width_ratio=(1, 3),
            )
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

        exercise_minutes = self.analytics.sum(
            display_exercise,
            "duration_minutes",
        )
        latest_sleep = (
            self.analytics.latest_value(
                display_health,
                "sleep_hours",
            )
            or 0
        )
        latest_mood = (
            self.analytics.latest_value(
                display_mental,
                "mood_score",
            )
            or 0
        )
        recorded_calories = self.analytics.sum(
            display_nutrition,
            "calories",
        )

        DashboardLayout.render_kpi_row(
            [
                {
                    "label": "🏃 Exercise",
                    "value": f"{exercise_minutes:.0f} min",
                    "delta": self.analytics.format_change(
                        self.analytics.percent_change_for_frame(
                            display_exercise,
                            "duration_minutes",
                        )
                    ),
                    "help": (
                        "Total exercise minutes for "
                        "the selected month."
                    ),
                },
                {
                    "label": "❤️ Sleep",
                    "value": f"{latest_sleep:.1f} hr",
                    "delta": self.analytics.format_change(
                        self.analytics.percent_change_for_frame(
                            display_health,
                            "sleep_hours",
                        )
                    ),
                    "help": (
                        "Latest sleep duration within "
                        "the selected month."
                    ),
                },
                {
                    "label": "😊 Mood",
                    "value": f"{latest_mood:.1f}/10",
                    "delta": self.analytics.format_change(
                        self.analytics.percent_change_for_frame(
                            display_mental,
                            "mood_score",
                        )
                    ),
                    "help": (
                        "Latest mood score within the "
                        "selected month."
                    ),
                },
                {
                    "label": "🥗 Nutrition",
                    "value": f"{recorded_calories:.0f} kcal",
                    "delta": self.analytics.format_change(
                        self.analytics.percent_change_for_frame(
                            display_nutrition,
                            "calories",
                        )
                    ),
                    "help": (
                        "Total recorded calories for "
                        "the selected month."
                    ),
                },
            ]
        )

        DashboardLayout.render_section_title(
            "Domain trends",
            (
                "Hover over any point to inspect "
                "the exact date and value."
            ),
        )

        charts = []

        if not display_exercise.empty:
            exercise_figure = px.line(
                display_exercise,
                x="recorded_on",
                y="duration_minutes",
                markers=True,
                labels={
                    "recorded_on": "Date",
                    "duration_minutes": "Minutes",
                },
            )
            exercise_figure.update_traces(
                hovertemplate=(
                    "<b>%{x|%B %d, %Y}</b><br>"
                    "Exercise: %{y:.0f} minutes"
                    "<extra></extra>"
                )
            )
            self._style_figure(
                exercise_figure,
                exercise_is_sample,
            )
            charts.append(
                (
                    "Exercise duration",
                    exercise_figure,
                    PLOTLY_CONFIG,
                )
            )

        if not display_health.empty:
            health_figure = px.line(
                display_health,
                x="recorded_on",
                y=[
                    "sleep_hours",
                    "sleep_quality",
                ],
                markers=True,
            )
            self._style_figure(
                health_figure,
                health_is_sample,
            )
            charts.append(
                (
                    "Sleep and recovery",
                    health_figure,
                    PLOTLY_CONFIG,
                )
            )

        if not display_mental.empty:
            mental_figure = px.line(
                display_mental,
                x="recorded_on",
                y=[
                    "mood_score",
                    "stress_score",
                    "energy_score",
                ],
                markers=True,
            )
            mental_figure.update_yaxes(
                range=[0, 10]
            )
            self._style_figure(
                mental_figure,
                mental_is_sample,
            )
            charts.append(
                (
                    "Mental wellness",
                    mental_figure,
                    PLOTLY_CONFIG,
                )
            )

        if not display_nutrition.empty:
            nutrition_figure = px.bar(
                display_nutrition,
                x="recorded_on",
                y="calories",
            )
            nutrition_figure.update_traces(
                hovertemplate=(
                    "<b>%{x|%B %d, %Y}</b><br>"
                    "Calories: %{y:,.0f}"
                    "<extra></extra>"
                )
            )
            self._style_figure(
                nutrition_figure,
                nutrition_is_sample,
            )
            charts.append(
                (
                    "Nutrition",
                    nutrition_figure,
                    PLOTLY_CONFIG,
                )
            )

        DashboardLayout.render_chart_grid(
            charts=charts,
            columns_per_row=2,
        )
