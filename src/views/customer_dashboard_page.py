import pandas as pd
import plotly.express as px
import streamlit as st

from components.layout import DashboardLayout
from services.analytics_service import AnalyticsService
from utilities.month_filter import MonthFilter


class CustomerDashboardPage:
    def __init__(self, exercise, health, mental, nutrition) -> None:
        self.repositories = {
            "exercise": exercise,
            "health": health,
            "mental": mental,
            "nutrition": nutrition,
        }
        self.analytics = AnalyticsService()

    def render(self, domain: str, client_id: int | None, client: dict | None = None) -> None:
        titles = {
            "exercise": "🏃 Exercise Dashboard",
            "health": "❤️ Health Dashboard",
            "mental": "😊 Mental Wellness Dashboard",
            "nutrition": "🥗 Nutrition Dashboard",
        }
        DashboardLayout.render_client_header(client, titles[domain])

        if client_id is None:
            st.info("Select a client to view this dashboard.")
            return

        frame = self.repositories[domain].list_for_client(client_id)

        if frame.empty:
            st.info("No records are available for this client yet.")
            return

        display, month = MonthFilter.filter(frame, MonthFilter.ALL_MONTHS), MonthFilter.ALL_MONTHS
        month = DashboardLayout.render_filter_bar(
            render_filter=lambda: MonthFilter.select_month(
                frame,
                key=f"{domain}_dashboard_month",
                label="Display month",
            ),
            width_ratio=(1, 4),
        )
        display = MonthFilter.filter(frame, month)

        if display.empty:
            st.warning("No records exist for the selected month.")
            return

        if domain == "exercise":
            cols = st.columns(3)
            cols[0].metric("Total minutes", f"{display['duration_minutes'].sum():.0f}")
            cols[1].metric("Average session", f"{display['duration_minutes'].mean():.1f} min")
            cols[2].metric("Calories burned", f"{display['calories_burned'].sum():.0f}")
            first = px.line(display, x="recorded_on", y="duration_minutes", markers=True)
            grouped = display.groupby("exercise_type", as_index=False)["duration_minutes"].sum()
            second = px.bar(grouped, x="exercise_type", y="duration_minutes")
        elif domain == "health":
            cols = st.columns(3)
            cols[0].metric("Latest sleep", f"{display.iloc[-1]['sleep_hours']:.1f} hr")
            cols[1].metric("Sleep quality", f"{display.iloc[-1]['sleep_quality']:.0f}/10")
            cols[2].metric("Latest weight", f"{display.iloc[-1]['weight_kg']:.1f} kg")
            first = px.line(display, x="recorded_on", y=["sleep_hours", "sleep_quality"], markers=True)
            second = px.line(display, x="recorded_on", y="weight_kg", markers=True)
        elif domain == "mental":
            cols = st.columns(3)
            cols[0].metric("Latest mood", f"{display.iloc[-1]['mood_score']:.0f}/10")
            cols[1].metric("Latest stress", f"{display.iloc[-1]['stress_score']:.0f}/10")
            cols[2].metric("Latest energy", f"{display.iloc[-1]['energy_score']:.0f}/10")
            first = px.line(
                display,
                x="recorded_on",
                y=["mood_score", "stress_score", "energy_score", "focus_score"],
                markers=True,
            )
            first.update_yaxes(range=[0, 10])
            averages = display[["mood_score", "stress_score", "energy_score", "focus_score"]].mean().reset_index()
            averages.columns = ["metric", "average_score"]
            second = px.bar(averages, x="metric", y="average_score")
            second.update_yaxes(range=[0, 10])
        else:
            cols = st.columns(3)
            cols[0].metric("Average calories", f"{display['calories'].mean():.0f}")
            cols[1].metric("Average protein", f"{display['protein_g'].mean():.1f} g")
            cols[2].metric("Entries", len(display))
            first = px.line(display, x="recorded_on", y="calories", markers=True)
            macros = display[["protein_g", "carbs_g", "fat_g"]].sum().reset_index()
            macros.columns = ["nutrient", "grams"]
            second = px.pie(macros, names="nutrient", values="grams")

        left, right = st.columns(2)
        left.plotly_chart(first, use_container_width=True)
        right.plotly_chart(second, use_container_width=True)
        st.subheader("Recent records")
        st.dataframe(display.tail(10), use_container_width=True, hide_index=True)
