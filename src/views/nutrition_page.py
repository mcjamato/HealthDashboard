from datetime import date

import streamlit as st

from models.domain_models import NutritionRecord
from views.shared import PageSupport


class NutritionPage:
    def __init__(self, repository) -> None:
        self.repository = repository

    def render(self, client_id: int | None, role: str) -> None:
        st.title("🥗 Nutrition Entry")
        if not PageSupport.require_client(client_id):
            return

        with st.form("nutrition_form", clear_on_submit=True):
            recorded_on = st.date_input("Date", date.today())
            meal_type = st.selectbox(
                "Meal type",
                ["Breakfast", "Lunch", "Dinner", "Snack", "Daily total"],
            )
            calories = st.number_input("Calories", 0.0, 10000.0, 0.0, step=10.0)
            protein = st.number_input("Protein (g)", 0.0, 1000.0, 0.0)
            carbs = st.number_input("Carbohydrates (g)", 0.0, 2000.0, 0.0)
            fat = st.number_input("Fat (g)", 0.0, 1000.0, 0.0)
            fiber = st.number_input("Fiber (g)", 0.0, 500.0, 0.0)
            water = st.number_input("Water (liters)", 0.0, 20.0, 0.0, step=0.25)
            notes = st.text_area("Notes")
            submitted = st.form_submit_button(
                "Save nutrition record", use_container_width=True
            )

        if submitted:
            self.repository.create(
                NutritionRecord(
                    int(client_id),
                    recorded_on,
                    meal_type,
                    calories,
                    protein,
                    carbs,
                    fat,
                    fiber,
                    water,
                    notes,
                ).to_dict()
            )
            st.success("Nutrition record saved.")
            st.rerun()

        frame = self.repository.list_for_client(int(client_id))
        PageSupport.show_history(frame, "Nutrition history")
        if role == "admin":
            PageSupport.admin_deactivate(self.repository, frame, "nutrition")
