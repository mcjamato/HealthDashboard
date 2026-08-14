from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

from components.layout import DashboardLayout
from services.analytics_service import AnalyticsService
from utilities.month_filter import MonthFilter


PLOTLY_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "responsive": True,
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
}


class DashboardPage:
    def __init__(self, exercise, health, mental, nutrition) -> None:
        self.exercise_repository = exercise
        self.health_repository = health
        self.mental_repository = mental
        self.nutrition_repository = nutrition
        self.analytics = AnalyticsService()

    @staticmethod
    def _dates(days: int = 180):
        start = date.today() - timedelta(days=days - 1)
        return [start + timedelta(days=i) for i in range(days)]

    def _samples(self):
        dates = self._dates()
        return {
            "exercise": pd.DataFrame(
                {
                    "recorded_on": dates,
                    "duration_minutes": [25 + (i % 7) * 4 for i in range(len(dates))],
                }
            ),
            "health": pd.DataFrame(
                {
                    "recorded_on": dates,
                    "sleep_hours": [
                        round(6.7 + (i / len(dates)) * 0.9 + (i % 5) * 0.05, 1)
                        for i in range(len(dates))
                    ],
                    "sleep_quality": [min(10, 6 + i // 45) for i in range(len(dates))],
                }
            ),
            "mental": pd.DataFrame(
                {
                    "recorded_on": dates,
                    "mood_score": [min(10, 5 + i // 40) for i in range(len(dates))],
                    "stress_score": [max(2, 8 - i // 45) for i in range(len(dates))],
                    "energy_score": [min(10, 5 + i // 45) for i in range(len(dates))],
                }
            ),
            "nutrition": pd.DataFrame(
                {
                    "recorded_on": dates,
                    "calories": [1950 + (i % 7) * 45 for i in range(len(dates))],
                }
            ),
        }

    def render(self, client_id: int | None, client: dict | None = None) -> None:
        DashboardLayout.render_client_header(client, "📊 Dashboard")

        samples = self._samples()
        exercise = (
            self.exercise_repository.list_for_client(client_id)
            if client_id is not None
            else pd.DataFrame()
        )
        health = (
            self.health_repository.list_for_client(client_id)
            if client_id is not None
            else pd.DataFrame()
        )
        mental = (
            self.mental_repository.list_for_client(client_id)
            if client_id is not None
            else pd.DataFrame()
        )
        nutrition = (
            self.nutrition_repository.list_for_client(client_id)
            if client_id is not None
            else pd.DataFrame()
        )

        display_exercise = samples["exercise"] if exercise.empty else exercise
        display_health = samples["health"] if health.empty else health
        display_mental = samples["mental"] if mental.empty else mental
        display_nutrition = samples["nutrition"] if nutrition.empty else nutrition

        available_dates = pd.concat(
            [
                frame[["recorded_on"]]
                for frame in [
                    display_exercise,
                    display_health,
                    display_mental,
                    display_nutrition,
                ]
            ],
            ignore_index=True,
        )

        month = DashboardLayout.render_filter_bar(
            render_filter=lambda: MonthFilter.select_month(
                available_dates,
                key="main_dashboard_month",
                label="Display month",
            ),
            width_ratio=(1, 4),
        )

        display_exercise = MonthFilter.filter(display_exercise, month)
        display_health = MonthFilter.filter(display_health, month)
        display_mental = MonthFilter.filter(display_mental, month)
        display_nutrition = MonthFilter.filter(display_nutrition, month)

        DashboardLayout.render_kpi_row(
            [
                {
                    "label": "🏃 Exercise",
                    "value": f"{self.analytics.sum(display_exercise, 'duration_minutes'):.0f} min",
                    "delta": self.analytics.format_change(
                        self.analytics.percent_change_for_frame(
                            display_exercise, "duration_minutes"
                        )
                    ),
                },
                {
                    "label": "❤️ Sleep",
                    "value": f"{(self.analytics.latest_value(display_health, 'sleep_hours') or 0):.1f} hr",
                    "delta": self.analytics.format_change(
                        self.analytics.percent_change_for_frame(
                            display_health, "sleep_hours"
                        )
                    ),
                },
                {
                    "label": "😊 Mood",
                    "value": f"{(self.analytics.latest_value(display_mental, 'mood_score') or 0):.1f}/10",
                    "delta": self.analytics.format_change(
                        self.analytics.percent_change_for_frame(
                            display_mental, "mood_score"
                        )
                    ),
                },
                {
                    "label": "🥗 Nutrition",
                    "value": f"{self.analytics.sum(display_nutrition, 'calories'):.0f} kcal",
                    "delta": self.analytics.format_change(
                        self.analytics.percent_change_for_frame(
                            display_nutrition, "calories"
                        )
                    ),
                },
            ]
        )

        charts = []

        if not display_exercise.empty:
            fig = px.line(
                display_exercise,
                x="recorded_on",
                y="duration_minutes",
                markers=True,
            )
            fig.update_traces(
                hovertemplate=(
                    "<b>%{x|%B %d, %Y}</b><br>"
                    "Exercise: %{y:.0f} minutes<extra></extra>"
                )
            )
            charts.append(("Exercise duration", fig, PLOTLY_CONFIG))

        if not display_health.empty:
            fig = px.line(
                display_health,
                x="recorded_on",
                y=["sleep_hours", "sleep_quality"],
                markers=True,
            )
            charts.append(("Sleep and recovery", fig, PLOTLY_CONFIG))

        if not display_mental.empty:
            fig = px.line(
                display_mental,
                x="recorded_on",
                y=["mood_score", "stress_score", "energy_score"],
                markers=True,
            )
            fig.update_yaxes(range=[0, 10])
            charts.append(("Mental wellness", fig, PLOTLY_CONFIG))

        if not display_nutrition.empty:
            fig = px.bar(
                display_nutrition,
                x="recorded_on",
                y="calories",
            )
            fig.update_traces(
                hovertemplate=(
                    "<b>%{x|%B %d, %Y}</b><br>"
                    "Calories: %{y:,.0f}<extra></extra>"
                )
            )
            charts.append(("Nutrition", fig, PLOTLY_CONFIG))

        DashboardLayout.render_chart_grid(charts, 2)

        if any([exercise.empty, health.empty, mental.empty, nutrition.empty]):
            st.info(
                "One or more dashboard panels use sample data until real records are available."
            )
