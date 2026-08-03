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


class CustomerDashboardPage:
    """Displays domain charts without showing data-entry controls."""

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
    def _dates() -> list[date]:
        start = date.today() - timedelta(days=6)
        return [
            start + timedelta(days=offset)
            for offset in range(7)
        ]

    def _sample_data(
        self,
        domain: str,
    ) -> pd.DataFrame:
        dates = self._dates()

        samples = {
            "exercise": pd.DataFrame(
                {
                    "recorded_on": dates,
                    "duration_minutes": [
                        20, 35, 25, 45, 30, 50, 40
                    ],
                    "calories_burned": [
                        120, 220, 155, 310, 190, 360, 275
                    ],
                    "exercise_type": [
                        "Walking",
                        "Running",
                        "Strength",
                        "Cycling",
                        "Walking",
                        "Sports",
                        "Strength",
                    ],
                }
            ),
            "health": pd.DataFrame(
                {
                    "recorded_on": dates,
                    "sleep_hours": [
                        6.8, 7.2, 7.0, 7.7, 7.4, 8.0, 7.8
                    ],
                    "sleep_quality": [
                        6, 7, 7, 8, 7, 9, 8
                    ],
                    "weight_kg": [
                        82.0, 81.9, 81.8, 81.8, 81.6, 81.5, 81.4
                    ],
                }
            ),
            "mental": pd.DataFrame(
                {
                    "recorded_on": dates,
                    "mood_score": [
                        6, 7, 6, 8, 7, 9, 8
                    ],
                    "stress_score": [
                        7, 6, 6, 5, 5, 4, 4
                    ],
                    "energy_score": [
                        5, 6, 6, 7, 7, 8, 8
                    ],
                    "focus_score": [
                        5, 6, 7, 7, 7, 8, 8
                    ],
                }
            ),
            "nutrition": pd.DataFrame(
                {
                    "recorded_on": dates,
                    "calories": [
                        2050, 1980, 2150, 2020, 2080, 2200, 2100
                    ],
                    "protein_g": [
                        95, 105, 100, 115, 110, 120, 118
                    ],
                    "carbs_g": [
                        240, 220, 260, 230, 245, 270, 250
                    ],
                    "fat_g": [
                        65, 60, 70, 62, 64, 72, 66
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
    ) -> None:
        titles = {
            "exercise": "🏃 Exercise Dashboard",
            "health": "❤️ Health Dashboard",
            "mental": "😊 Mental Wellness Dashboard",
            "nutrition": "🥗 Nutrition Dashboard",
        }

        st.title(titles[domain])
        st.caption(
            "This page is for viewing analytics only. "
            "Use Customer Data to enter new records."
        )

        if client_id is None:
            frame = pd.DataFrame()
        else:
            frame = self.repositories[
                domain
            ].list_for_client(client_id)

        sample = frame.empty
        display = (
            self._sample_data(domain)
            if sample
            else self.analytics.prepare_chronological(frame)
        )

        if sample:
            st.info(
                "Sample data is displayed until this "
                "customer has real records."
            )

        if domain == "exercise":
            metric_columns = st.columns(3)
            metric_columns[0].metric(
                "Total minutes",
                f"{display['duration_minutes'].sum():.0f}",
            )
            metric_columns[1].metric(
                "Average session",
                f"{display['duration_minutes'].mean():.1f} min",
            )
            metric_columns[2].metric(
                "Calories burned",
                f"{display['calories_burned'].sum():.0f}",
            )

            line = px.line(
                display,
                x="recorded_on",
                y="duration_minutes",
                markers=True,
                title="Exercise duration trend",
            )
            bar = px.bar(
                display,
                x="exercise_type",
                y="duration_minutes",
                title="Exercise minutes by activity",
            )

        elif domain == "health":
            metric_columns = st.columns(3)
            metric_columns[0].metric(
                "Latest sleep",
                f"{display['sleep_hours'].iloc[-1]:.1f} hr",
            )
            metric_columns[1].metric(
                "Sleep quality",
                f"{display['sleep_quality'].iloc[-1]:.0f}/10",
            )
            metric_columns[2].metric(
                "Latest weight",
                f"{display['weight_kg'].iloc[-1]:.1f} kg",
            )

            line = px.line(
                display,
                x="recorded_on",
                y=["sleep_hours", "sleep_quality"],
                markers=True,
                title="Sleep duration and quality",
            )
            bar = px.line(
                display,
                x="recorded_on",
                y="weight_kg",
                markers=True,
                title="Weight trend",
            )

        elif domain == "mental":
            metric_columns = st.columns(3)
            metric_columns[0].metric(
                "Latest mood",
                f"{display['mood_score'].iloc[-1]:.0f}/10",
            )
            metric_columns[1].metric(
                "Latest stress",
                f"{display['stress_score'].iloc[-1]:.0f}/10",
            )
            metric_columns[2].metric(
                "Latest energy",
                f"{display['energy_score'].iloc[-1]:.0f}/10",
            )

            line = px.line(
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
            line.update_yaxes(range=[0, 10])

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

            bar = px.bar(
                averages,
                x="metric",
                y="average_score",
                title="Average wellness scores",
            )
            bar.update_yaxes(range=[0, 10])

        else:
            metric_columns = st.columns(3)
            metric_columns[0].metric(
                "Average calories",
                f"{display['calories'].mean():.0f}",
            )
            metric_columns[1].metric(
                "Average protein",
                f"{display['protein_g'].mean():.1f} g",
            )
            metric_columns[2].metric(
                "Entries",
                len(display),
            )

            line = px.line(
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

            bar = px.pie(
                macros,
                names="nutrient",
                values="grams",
                title="Macronutrient mix",
            )

        self._label_sample(
            line,
            sample,
        )
        self._label_sample(
            bar,
            sample,
        )

        left, right = st.columns(2)
        left.plotly_chart(
            line,
            use_container_width=True,
        )
        right.plotly_chart(
            bar,
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
