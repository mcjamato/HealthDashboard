from datetime import date

import streamlit as st

from models.domain_models import MentalWellnessRecord
from views.shared import PageSupport


class MentalWellnessPage:
    def __init__(self, repository) -> None:
        self.repository = repository

    def render(self, client_id: int | None, role: str) -> None:
        st.title("😊 Mental Wellness Entry")
        if not PageSupport.require_client(client_id):
            return

        with st.form("mental_form", clear_on_submit=True):
            recorded_on = st.date_input("Date", date.today())
            mood = st.slider("Mood", 1, 10, 7)
            stress = st.slider("Stress", 1, 10, 4)
            energy = st.slider("Energy", 1, 10, 7)
            focus = st.slider("Focus", 1, 10, 7)
            meditation = st.number_input("Meditation (minutes)", 0, 600, 0)
            journal = st.text_area("Journal entry")
            submitted = st.form_submit_button(
                "Save wellness record", width="stretch"
            )

        if submitted:
            self.repository.create(
                MentalWellnessRecord(
                    int(client_id),
                    recorded_on,
                    mood,
                    stress,
                    energy,
                    focus,
                    meditation,
                    journal,
                ).to_dict()
            )
            st.success("Mental wellness record saved.")
            st.rerun()

        frame = self.repository.list_for_client(int(client_id))
        PageSupport.show_history(frame, "Mental wellness history")
        if role == "admin":
            PageSupport.admin_deactivate(self.repository, frame, "mental")
