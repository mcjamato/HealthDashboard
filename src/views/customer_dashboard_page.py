import pandas as pd
import plotly.express as px
import streamlit as st

from components.layout import DashboardLayout
from services.analytics_service import AnalyticsService
from utilities.month_filter import MonthFilter


class CustomerDashboardPage:
    """Read-only single-domain customer dashboards."""

    def __init__(
        self,
        exercise,
        health,
        mental,
        nutrition,
    ) -> None:
        self.repositories = {
            "exercise": exercise,
            "health": health,
            "mental": mental,
            "nutrition": nutrition,
        }

        self.analytics = AnalyticsService()

    def render(
        self,
        domain: str,
        client_id: int | None,
        client: dict | None = None,
    ) -> None:
        titles = {
            "exercise": "🏃 Exercise Dashboard",
            "health": "❤️ Health Dashboard",
            "mental": "😊 Mental Wellness Dashboard",
            "nutrition": "🥗 Nutrition Dashboard",
        }

        DashboardLayout.render_client_header(
            client,
            titles[domain],
        )

        if client_id is None:
            st.info(
                "Select a client to view this dashboard."
            )
            return

        frame = self.repositories[
            domain
        ].list_for_client(
            client_id
        )

        if frame.empty:
            st.info(
                "No records are available for this client yet."
            )
            return

        selected_months = DashboardLayout.render_filter_bar(
            render_filter=lambda: (
                MonthFilter.select_months(
                    frame,
                    key_prefix=f"{domain}_dashboard",
                )
            ),
            title="Dashboard months",
            width_ratio=(
                1,
                4,
            ),
        )

        display = MonthFilter.filter(
            frame,
            selected_months,
        )

        if display.empty:
            st.warning(
                "No records exist for the selected month selection."
            )
            return

        selection_label = MonthFilter.selection_caption(
            selected_months
        )

        st.caption(
            f"Showing: {selection_label}"
        )

        charts = []

        if domain == "exercise":
            columns = st.columns(
                3
            )

            columns[0].metric(
                "Total minutes",
                f"{display['duration_minutes'].sum():.0f}",
            )

            columns[1].metric(
                "Average session",
                f"{display['duration_minutes'].mean():.1f} min",
            )

            columns[2].metric(
                "Calories burned",
                f"{display['calories_burned'].sum():.0f}",
            )

            first = px.line(
                display,
                x="recorded_on",
                y="duration_minutes",
                markers=True,
            )

            grouped = (
                display.groupby(
                    "exercise_type",
                    as_index=False,
                )[
                    "duration_minutes"
                ]
                .sum()
            )

            second = px.bar(
                grouped,
                x="exercise_type",
                y="duration_minutes",
            )

            charts = [
                (
                    "Exercise duration",
                    first,
                    display,
                    f"exercise_duration_{selection_label}",
                    "exercise_duration",
                ),
                (
                    "Minutes by activity",
                    second,
                    grouped,
                    f"exercise_activity_{selection_label}",
                    "exercise_activity",
                ),
            ]

        elif domain == "health":
            chronological = display.sort_values(
                "recorded_on"
            )

            latest = chronological.iloc[
                -1
            ]

            columns = st.columns(
                3
            )

            columns[0].metric(
                "Latest sleep",
                f"{latest['sleep_hours']:.1f} hr",
            )

            columns[1].metric(
                "Sleep quality",
                f"{latest['sleep_quality']:.0f}/10",
            )

            weight = latest.get(
                "weight_kg"
            )

            columns[2].metric(
                "Latest weight",
                (
                    f"{weight:.1f} kg"
                    if pd.notna(weight)
                    else "N/A"
                ),
            )

            first = px.line(
                display,
                x="recorded_on",
                y=[
                    "sleep_hours",
                    "sleep_quality",
                ],
                markers=True,
            )

            weight_data = display.dropna(
                subset=[
                    "weight_kg"
                ]
            )

            second = px.line(
                weight_data,
                x="recorded_on",
                y="weight_kg",
                markers=True,
            )

            charts = [
                (
                    "Sleep and quality",
                    first,
                    display,
                    f"health_sleep_{selection_label}",
                    "health_sleep",
                ),
                (
                    "Weight trend",
                    second,
                    weight_data,
                    f"health_weight_{selection_label}",
                    "health_weight",
                ),
            ]

        elif domain == "mental":
            chronological = display.sort_values(
                "recorded_on"
            )

            latest = chronological.iloc[
                -1
            ]

            columns = st.columns(
                3
            )

            columns[0].metric(
                "Latest mood",
                f"{latest['mood_score']:.0f}/10",
            )

            columns[1].metric(
                "Latest stress",
                f"{latest['stress_score']:.0f}/10",
            )

            columns[2].metric(
                "Latest energy",
                f"{latest['energy_score']:.0f}/10",
            )

            first = px.line(
                display,
                x="recorded_on",
                y=[
                    "mood_score",
                    "stress_score",
                    "energy_score",
                    "focus_score",
                ],
                markers=True,
            )

            first.update_yaxes(
                range=[
                    0,
                    10,
                ]
            )

            averages = (
                display[
                    [
                        "mood_score",
                        "stress_score",
                        "energy_score",
                        "focus_score",
                    ]
                ]
                .mean()
                .reset_index()
            )

            averages.columns = [
                "metric",
                "average_score",
            ]

            second = px.bar(
                averages,
                x="metric",
                y="average_score",
            )

            second.update_yaxes(
                range=[
                    0,
                    10,
                ]
            )

            charts = [
                (
                    "Mental wellness trends",
                    first,
                    display,
                    f"mental_trends_{selection_label}",
                    "mental_trends",
                ),
                (
                    "Average wellness scores",
                    second,
                    averages,
                    f"mental_averages_{selection_label}",
                    "mental_averages",
                ),
            ]

        else:
            columns = st.columns(
                3
            )

            columns[0].metric(
                "Average calories",
                f"{display['calories'].mean():.0f}",
            )

            columns[1].metric(
                "Average protein",
                f"{display['protein_g'].mean():.1f} g",
            )

            columns[2].metric(
                "Entries",
                len(display),
            )

            first = px.line(
                display,
                x="recorded_on",
                y="calories",
                markers=True,
            )

            macros = (
                display[
                    [
                        "protein_g",
                        "carbs_g",
                        "fat_g",
                    ]
                ]
                .sum()
                .reset_index()
            )

            macros.columns = [
                "nutrient",
                "grams",
            ]

            second = px.pie(
                macros,
                names="nutrient",
                values="grams",
            )

            charts = [
                (
                    "Calorie trend",
                    first,
                    display,
                    f"nutrition_calories_{selection_label}",
                    "nutrition_calories",
                ),
                (
                    "Macronutrient mix",
                    second,
                    macros,
                    f"nutrition_macros_{selection_label}",
                    "nutrition_macros",
                ),
            ]

        DashboardLayout.render_chart_grid(
            charts,
            2,
        )

        st.subheader(
            "Recent records"
        )

        st.dataframe(
            display.tail(
                10
            ),
            width="stretch",
            hide_index=True,
        )
