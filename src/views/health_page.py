from datetime import date

import streamlit as st

from models.domain_models import HealthRecord
from views.shared import PageSupport


class HealthPage:
    def __init__(self, repository) -> None:
        self.repository = repository

    def render(self, client_id: int | None, role: str) -> None:
        st.title("❤️ Health Entry")
        if not PageSupport.require_client(client_id):
            return

        with st.form("health_form", clear_on_submit=True):
            recorded_on = st.date_input("Date", date.today())
            weight = st.number_input("Weight (kg)", 0.0, 500.0, 0.0, step=0.1)
            sleep = st.number_input("Sleep (hours)", 0.0, 24.0, 8.0, step=0.25)
            quality = st.slider("Sleep quality", 1, 10, 7)
            heart_rate = st.number_input("Resting heart rate", 0, 250, 0)
            left, right = st.columns(2)
            systolic = left.number_input("Systolic BP", 0, 300, 0)
            diastolic = right.number_input("Diastolic BP", 0, 200, 0)
            water = st.number_input("Water (liters)", 0.0, 20.0, 0.0, step=0.25)
            notes = st.text_area("Notes")
            submitted = st.form_submit_button(
                "Save health record", width="stretch"
            )

        if submitted:
            self.repository.create(
                HealthRecord(
                    int(client_id),
                    recorded_on,
                    weight or None,
                    sleep or None,
                    quality,
                    heart_rate or None,
                    systolic or None,
                    diastolic or None,
                    water,
                    notes,
                ).to_dict()
            )
            st.success("Health record saved.")
            st.rerun()

        frame = self.repository.list_for_client(int(client_id))
        PageSupport.show_history(frame, "Health history")
        if role == "admin":
            PageSupport.admin_deactivate(self.repository, frame, "health")
