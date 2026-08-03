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
from views.client_header import ClientHeader


class CustomerDashboardPage:
    """Displays read-only domain dashboards with monthly filtering."""

    def __init__(
        self,
        exercise_repository: ExerciseRepository,
        health_repository: HealthRepository,
        mental_repository: MentalWellnessRepository,
        nutrition_repository: NutritionRepository,
    ) -> None:
        self.repositories = {
            "exercise": exercise_repository,
            "health": health_repository,
            "mental": mental_repository,
            "nutrition": nutrition_repository,
        }

        self.analytics = AnalyticsService()

    @staticmethod
    def _dates(
        days: int = 180,
    ) -> list[date]:
        """Return six months of sample dates."""

        start = date.today() - timedelta(
            days=days - 1
        )

        return [
            start + timedelta(days=offset)
            for offset in range(days)
        ]

    def _sample_data(
        self,
        domain: str,
    ) -> pd.DataFrame:
        """Create six months of sample data for one domain."""

        dates = self._dates()

        samples = {
            "exercise": pd.DataFrame(
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
                    "exercise_type": [
                        [
                            "Walking",
                            "Running",
                            "Strength",
                            "Cycling",
                            "Yoga",
                            "Sports",
                        ][index % 6]
                        for index in range(len(dates))
                    ],
                }
            ),
            "health": pd.DataFrame(
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
                    "weight_kg": [
                        round(
                            82.0 - index * 0.01,
                            1,
                        )
                        for index in range(len(dates))
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
                    "focus_score": [
                        min(
                            10,
                            6 + index // 50,
                        )
                        for index in range(len(dates))
                    ],
                }
            ),
            "nutrition": pd.DataFrame(
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
                    "carbs_g": [
                        220 + (index % 5) * 10
                        for index in range(len(dates))
                    ],
                    "fat_g": [
                        60 + (index % 4) * 3
                        for index in range(len(dates))
                    ],
                }
            ),
        }

        return samples[domain]

    @staticmethod
    def _label_sample(
        figure,
        sample: bool,
    ) -> None:
        """Add shared chart spacing and sample labeling."""

        figure.update_layout(
            margin={
                "l": 20,
                "r": 20,
                "t": 65,
                "b": 20,
            }
        )

        if sample:
            figure.add_annotation(
                text="SAMPLE DATA",
                xref="paper",
                yref="paper",
                x=1,
                y=1.13,
                showarrow=False,
            )

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

        ClientHeader.render(
            client=client,
            page_label=titles[domain],
        )

        st.caption(
            "This page is read-only. Use Customer "
            "Data to add new records."
        )

        if client_id is None:
            frame = pd.DataFrame()
        else:
            frame = (
                self.repositories[domain]
                .list_for_client(client_id)
            )

        sample = frame.empty

        display = (
            self._sample_data(domain)
            if sample
            else self.analytics
            .prepare_chronological(frame)
        )

        if sample:
            st.info(
                "Sample data is displayed until this "
                "customer has real records."
            )

        display, selected_month = MonthFilter.apply(
            frame=display,
            key=f"{domain}_dashboard_month",
            label="Display month",
        )

        st.caption(
            f"Showing: {selected_month}"
        )

        if display.empty:
            st.warning(
                "No records are available for the "
                "selected month."
            )
            return

        if domain == "exercise":
            columns = st.columns(3)

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

            first_chart = px.line(
                display,
                x="recorded_on",
                y="duration_minutes",
                markers=True,
                title="Exercise duration trend",
            )

            grouped_exercise = (
                display.groupby(
                    "exercise_type",
                    as_index=False,
                )["duration_minutes"]
                .sum()
            )

            second_chart = px.bar(
                grouped_exercise,
                x="exercise_type",
                y="duration_minutes",
                title="Exercise minutes by activity",
            )

        elif domain == "health":
            columns = st.columns(3)

            columns[0].metric(
                "Latest sleep",
                f"{display['sleep_hours'].iloc[-1]:.1f} hr",
            )

            columns[1].metric(
                "Sleep quality",
                f"{display['sleep_quality'].iloc[-1]:.0f}/10",
            )

            columns[2].metric(
                "Latest weight",
                f"{display['weight_kg'].iloc[-1]:.1f} kg",
            )

            first_chart = px.line(
                display,
                x="recorded_on",
                y=[
                    "sleep_hours",
                    "sleep_quality",
                ],
                markers=True,
                title="Sleep duration and quality",
            )

            second_chart = px.line(
                display,
                x="recorded_on",
                y="weight_kg",
                markers=True,
                title="Weight trend",
            )

        elif domain == "mental":
            columns = st.columns(3)

            columns[0].metric(
                "Latest mood",
                f"{display['mood_score'].iloc[-1]:.0f}/10",
            )

            columns[1].metric(
                "Latest stress",
                f"{display['stress_score'].iloc[-1]:.0f}/10",
            )

            columns[2].metric(
                "Latest energy",
                f"{display['energy_score'].iloc[-1]:.0f}/10",
            )

            first_chart = px.line(
                display,
                x="recorded_on",
                y=[
                    "mood_score",
                    "stress_score",
                    "energy_score",
                    "focus_score",
                ],
                markers=True,
                title="Mental wellness trends",
            )

            first_chart.update_yaxes(
                range=[0, 10]
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

            second_chart = px.bar(
                averages,
                x="metric",
                y="average_score",
                title="Average wellness scores",
            )

            second_chart.update_yaxes(
                range=[0, 10]
            )

        else:
            columns = st.columns(3)

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

            first_chart = px.line(
                display,
                x="recorded_on",
                y="calories",
                markers=True,
                title="Calorie trend",
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

            second_chart = px.pie(
                macros,
                names="nutrient",
                values="grams",
                title="Macronutrient mix",
            )

        self._label_sample(
            first_chart,
            sample,
        )

        self._label_sample(
            second_chart,
            sample,
        )

        left, right = st.columns(2)

        left.plotly_chart(
            first_chart,
            use_container_width=True,
        )

        right.plotly_chart(
            second_chart,
            use_container_width=True,
        )

        st.subheader("Recent records")

        if sample:
            st.caption(
                "The preview table contains sample values."
            )

        st.dataframe(
            display.tail(10),
            use_container_width=True,
            hide_index=True,
        )
