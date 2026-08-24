from datetime import date

import plotly.express as px
import streamlit as st

from models.domain_models import ExerciseRecord
from services.analytics_service import AnalyticsService
from views.shared import PageSupport


class ExercisePage:
    def __init__(self, repository) -> None:
        self.repository = repository
        self.analytics = AnalyticsService()

    def render(self, client_id: int | None, role: str) -> None:
        st.title("🏃 Exercise Entry")
        if not PageSupport.require_client(client_id):
            return

        with st.form("exercise_form", clear_on_submit=True):
            recorded_on = st.date_input("Date", date.today())
            exercise_type = st.selectbox(
                "Exercise type",
                ["Walking", "Running", "Cycling", "Strength", "Sports", "Other"],
            )
            duration = st.number_input("Duration (minutes)", 0, 600, 30)
            intensity = st.selectbox("Intensity", ["Low", "Moderate", "High"])
            steps = st.number_input("Steps", 0, 100000, 0)
            distance = st.number_input(
                "Distance (km)", 0.0, 500.0, 0.0, step=0.1
            )
            calories = st.number_input(
                "Calories burned", 0.0, 5000.0, 0.0, step=10.0
            )
            notes = st.text_area("Notes")
            submitted = st.form_submit_button(
                "Save exercise record", width="stretch"
            )

        if submitted:
            self.repository.create(
                ExerciseRecord(
                    int(client_id),
                    recorded_on,
                    exercise_type,
                    duration,
                    intensity,
                    steps,
                    distance,
                    calories,
                    notes,
                ).to_dict()
            )
            st.success("Exercise record saved.")
            st.rerun()

        frame = self.repository.list_for_client(int(client_id))
        PageSupport.show_history(frame, "Exercise history")
        if role == "admin":
            PageSupport.admin_deactivate(self.repository, frame, "exercise")
