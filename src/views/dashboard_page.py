from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

from components.layout import DashboardLayout
from services.analytics_service import AnalyticsService
from utilities.month_filter import MonthFilter


class DashboardPage:
    """Main four-domain client dashboard."""

    def __init__(
        self,
        exercise,
        health,
        mental,
        nutrition,
    ) -> None:
        self.exercise_repository = exercise
        self.health_repository = health
        self.mental_repository = mental
        self.nutrition_repository = nutrition
        self.analytics = AnalyticsService()

    @staticmethod
    def _dates(
        days: int = 180,
    ):
        start = (
            date.today()
            - timedelta(
                days=days - 1
            )
        )

        return [
            start + timedelta(
                days=index
            )
            for index in range(
                days
            )
        ]

    def _samples(
        self,
    ):
        dates = self._dates()

        return {
            "exercise": pd.DataFrame(
                {
                    "recorded_on": dates,
                    "duration_minutes": [
                        25 + (index % 7) * 4
                        for index in range(
                            len(dates)
                        )
                    ],
                }
            ),
            "health": pd.DataFrame(
                {
                    "recorded_on": dates,
                    "sleep_hours": [
                        round(
                            6.7
                            + (
                                index
                                / len(dates)
                            )
                            * 0.9
                            + (
                                index % 5
                            )
                            * 0.05,
                            1,
                        )
                        for index in range(
                            len(dates)
                        )
                    ],
                    "sleep_quality": [
                        min(
                            10,
                            6 + index // 45,
                        )
                        for index in range(
                            len(dates)
                        )
                    ],
                }
            ),
            "mental": pd.DataFrame(
                {
                    "recorded_on": dates,
                    "mood_score": [
                        min(
                            10,
                            5 + index // 40,
                        )
                        for index in range(
                            len(dates)
                        )
                    ],
                    "stress_score": [
                        max(
                            2,
                            8 - index // 45,
                        )
                        for index in range(
                            len(dates)
                        )
                    ],
                    "energy_score": [
                        min(
                            10,
                            5 + index // 45,
                        )
                        for index in range(
                            len(dates)
                        )
                    ],
                }
            ),
            "nutrition": pd.DataFrame(
                {
                    "recorded_on": dates,
                    "calories": [
                        1950
                        + (index % 7) * 45
                        for index in range(
                            len(dates)
                        )
                    ],
                }
            ),
        }

    def render(
        self,
        client_id: int | None,
        client: dict | None = None,
        role: str = "client",
        client_details: dict | None = None,
    ) -> None:
        DashboardLayout.render_client_header(
            client,
            "📊 Dashboard",
        )

        if (
            role == "admin"
            and client_details
        ):
            with st.expander(
                "View full client intake information",
                expanded=False,
            ):
                left, right = st.columns(
                    2
                )

                with left:
                    st.markdown(
                        f"**Client ID:** "
                        f"{client_details.get('id', 'Not available')}"
                    )
                    st.markdown(
                        f"**First name:** "
                        f"{client_details.get('first_name', 'Not available')}"
                    )
                    st.markdown(
                        f"**Last name:** "
                        f"{client_details.get('last_name', 'Not available')}"
                    )
                    st.markdown(
                        f"**Email:** "
                        f"{client_details.get('email', 'Not provided')}"
                    )

                with right:
                    st.markdown(
                        f"**Birth date:** "
                        f"{client_details.get('birth_date', 'Not provided')}"
                    )
                    st.markdown(
                        f"**Age:** "
                        f"{client.get('age', 'Not available') if client else 'Not available'}"
                    )
                    st.markdown(
                        f"**Created:** "
                        f"{client_details.get('created_at', 'Not available')}"
                    )
                    st.markdown(
                        "**Status:** Active"
                    )

                st.caption(
                    "This section displays all intake fields "
                    "currently stored in the client profile."
                )

        samples = self._samples()

        exercise = (
            self.exercise_repository
            .list_for_client(
                client_id
            )
            if client_id is not None
            else pd.DataFrame()
        )

        health = (
            self.health_repository
            .list_for_client(
                client_id
            )
            if client_id is not None
            else pd.DataFrame()
        )

        mental = (
            self.mental_repository
            .list_for_client(
                client_id
            )
            if client_id is not None
            else pd.DataFrame()
        )

        nutrition = (
            self.nutrition_repository
            .list_for_client(
                client_id
            )
            if client_id is not None
            else pd.DataFrame()
        )

        display_exercise = (
            samples["exercise"]
            if exercise.empty
            else exercise
        )

        display_health = (
            samples["health"]
            if health.empty
            else health
        )

        display_mental = (
            samples["mental"]
            if mental.empty
            else mental
        )

        display_nutrition = (
            samples["nutrition"]
            if nutrition.empty
            else nutrition
        )

        available_dates = pd.concat(
            [
                frame[
                    ["recorded_on"]
                ]
                for frame in [
                    display_exercise,
                    display_health,
                    display_mental,
                    display_nutrition,
                ]
            ],
            ignore_index=True,
        )

        selected_months = DashboardLayout.render_filter_bar(
            render_filter=lambda: (
                MonthFilter.select_months(
                    available_dates,
                    key_prefix="main_dashboard",
                )
            ),
            title="Dashboard months",
            width_ratio=(
                1,
                4,
            ),
        )

        display_exercise = MonthFilter.filter(
            display_exercise,
            selected_months,
        )
        display_health = MonthFilter.filter(
            display_health,
            selected_months,
        )
        display_mental = MonthFilter.filter(
            display_mental,
            selected_months,
        )
        display_nutrition = MonthFilter.filter(
            display_nutrition,
            selected_months,
        )

        selection_label = MonthFilter.selection_caption(
            selected_months
        )

        st.caption(
            f"Showing: {selection_label}"
        )

        DashboardLayout.render_kpi_row(
            [
                {
                    "label": "🏃 Exercise",
                    "value": (
                        f"{self.analytics.sum(display_exercise, 'duration_minutes'):.0f} min"
                    ),
                    "delta": (
                        self.analytics
                        .format_change(
                            self.analytics
                            .percent_change_for_frame(
                                display_exercise,
                                "duration_minutes",
                            )
                        )
                    ),
                },
                {
                    "label": "❤️ Sleep",
                    "value": (
                        f"{(self.analytics.latest_value(display_health, 'sleep_hours') or 0):.1f} hr"
                    ),
                    "delta": (
                        self.analytics
                        .format_change(
                            self.analytics
                            .percent_change_for_frame(
                                display_health,
                                "sleep_hours",
                            )
                        )
                    ),
                },
                {
                    "label": "😊 Mood",
                    "value": (
                        f"{(self.analytics.latest_value(display_mental, 'mood_score') or 0):.1f}/10"
                    ),
                    "delta": (
                        self.analytics
                        .format_change(
                            self.analytics
                            .percent_change_for_frame(
                                display_mental,
                                "mood_score",
                            )
                        )
                    ),
                },
                {
                    "label": "🥗 Nutrition",
                    "value": (
                        f"{self.analytics.sum(display_nutrition, 'calories'):.0f} kcal"
                    ),
                    "delta": (
                        self.analytics
                        .format_change(
                            self.analytics
                            .percent_change_for_frame(
                                display_nutrition,
                                "calories",
                            )
                        )
                    ),
                },
            ]
        )

        charts = []

        if not display_exercise.empty:
            figure = px.line(
                display_exercise,
                x="recorded_on",
                y="duration_minutes",
                markers=True,
            )

            figure.update_traces(
                hovertemplate=(
                    "<b>%{x|%B %d, %Y}</b><br>"
                    "Exercise: %{y:.0f} minutes"
                    "<extra></extra>"
                )
            )

            charts.append(
                (
                    "Exercise duration",
                    figure,
                    display_exercise,
                    f"exercise_{selection_label}",
                    "main_exercise",
                )
            )

        if not display_health.empty:
            figure = px.line(
                display_health,
                x="recorded_on",
                y=[
                    "sleep_hours",
                    "sleep_quality",
                ],
                markers=True,
            )

            charts.append(
                (
                    "Sleep and recovery",
                    figure,
                    display_health,
                    f"health_{selection_label}",
                    "main_health",
                )
            )

        if not display_mental.empty:
            figure = px.line(
                display_mental,
                x="recorded_on",
                y=[
                    "mood_score",
                    "stress_score",
                    "energy_score",
                ],
                markers=True,
            )

            figure.update_yaxes(
                range=[
                    0,
                    10,
                ]
            )

            charts.append(
                (
                    "Mental wellness",
                    figure,
                    display_mental,
                    f"mental_wellness_{selection_label}",
                    "main_mental",
                )
            )

        if not display_nutrition.empty:
            figure = px.bar(
                display_nutrition,
                x="recorded_on",
                y="calories",
            )

            figure.update_traces(
                hovertemplate=(
                    "<b>%{x|%B %d, %Y}</b><br>"
                    "Calories: %{y:,.0f}"
                    "<extra></extra>"
                )
            )

            charts.append(
                (
                    "Nutrition",
                    figure,
                    display_nutrition,
                    f"nutrition_{selection_label}",
                    "main_nutrition",
                )
            )

        DashboardLayout.render_chart_grid(
            charts,
            2,
        )

        if any(
            [
                exercise.empty,
                health.empty,
                mental.empty,
                nutrition.empty,
            ]
        ):
            st.info(
                "One or more dashboard panels use "
                "sample data until real records are available."
            )
