from datetime import date
import os

import pandas as pd
import streamlit as st

from models.domain_models import NutritionRecord
from services.food_vision_service import FoodVisionService
from views.shared import PageSupport


class NutritionPage:
    """Manual nutrition entry plus optional food-photo analysis."""

    def __init__(
        self,
        repository,
    ) -> None:
        self.repository = repository

    def render(
        self,
        client_id: int | None,
        role: str,
    ) -> None:
        st.title(
            "🥗 Nutrition Entry"
        )

        if not PageSupport.require_client(
            client_id
        ):
            return

        manual_tab, photo_tab = st.tabs(
            [
                "Manual Entry",
                "Food Photo Analyzer",
            ]
        )

        with manual_tab:
            self._render_manual_entry(
                int(client_id)
            )

        with photo_tab:
            self._render_photo_analyzer(
                int(client_id)
            )

        frame = self.repository.list_for_client(
            int(client_id)
        )

        PageSupport.show_history(
            frame,
            "Nutrition history",
        )

        if role == "admin":
            PageSupport.admin_deactivate(
                self.repository,
                frame,
                "nutrition",
            )

    def _render_manual_entry(
        self,
        client_id: int,
    ) -> None:
        with st.form(
            "nutrition_form",
            clear_on_submit=True,
        ):
            recorded_on = st.date_input(
                "Date",
                date.today(),
                key="nutrition_manual_date",
            )

            meal_type = st.selectbox(
                "Meal type",
                [
                    "Breakfast",
                    "Lunch",
                    "Dinner",
                    "Snack",
                    "Daily total",
                ],
                key="nutrition_manual_meal",
            )

            calories = st.number_input(
                "Calories",
                0.0,
                10000.0,
                0.0,
                step=10.0,
            )

            protein = st.number_input(
                "Protein (g)",
                0.0,
                1000.0,
                0.0,
            )

            carbs = st.number_input(
                "Carbohydrates (g)",
                0.0,
                2000.0,
                0.0,
            )

            fat = st.number_input(
                "Fat (g)",
                0.0,
                1000.0,
                0.0,
            )

            fiber = st.number_input(
                "Fiber (g)",
                0.0,
                500.0,
                0.0,
            )

            water = st.number_input(
                "Water (liters)",
                0.0,
                20.0,
                0.0,
                step=0.25,
            )

            notes = st.text_area(
                "Notes"
            )

            submitted = st.form_submit_button(
                "Save nutrition record",
                width="stretch",
            )

        if submitted:
            self.repository.create(
                NutritionRecord(
                    client_id,
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

            st.success(
                "Nutrition record saved."
            )
            st.rerun()

    @staticmethod
    def _get_openai_key(
    ) -> str | None:
        api_key = os.getenv(
            "OPENAI_API_KEY"
        )

        if api_key:
            return api_key

        try:
            value = st.secrets.get(
                "OPENAI_API_KEY"
            )
            return (
                str(value)
                if value
                else None
            )
        except (
            FileNotFoundError,
            KeyError,
        ):
            return None

    @staticmethod
    def _get_vision_model(
    ) -> str:
        model = os.getenv(
            "OPENAI_VISION_MODEL"
        )

        if model:
            return model

        try:
            value = st.secrets.get(
                "OPENAI_VISION_MODEL"
            )
            if value:
                return str(
                    value
                )
        except (
            FileNotFoundError,
            KeyError,
        ):
            pass

        return "gpt-5.6-luna"

    def _render_photo_analyzer(
        self,
        client_id: int,
    ) -> None:
        st.write(
            "Take a picture or upload a food photo. "
            "The result is an estimate based on visible "
            "foods and portions."
        )

        st.warning(
            "Photo-based calories and portion sizes are "
            "estimates and should not be treated as exact "
            "dietary or medical measurements."
        )

        api_key = self._get_openai_key()

        if not api_key:
            st.info(
                "Food-photo analysis is not configured yet. "
                "Add OPENAI_API_KEY to Streamlit Cloud Secrets "
                "to enable it."
            )
            return

        source = st.radio(
            "Image source",
            [
                "Camera",
                "Upload image",
            ],
            horizontal=True,
        )

        image_file = None

        if source == "Camera":
            image_file = st.camera_input(
                "Take a food photo",
                resolution="720p",
                width=480,
            )
        else:
            image_file = st.file_uploader(
                "Upload a food photo",
                type=[
                    "jpg",
                    "jpeg",
                    "png",
                    "webp",
                ],
                key="nutrition_food_photo",
                width="stretch",
            )

        if image_file is None:
            return

        st.image(
            image_file,
            caption="Food image to analyze",
            width=420,
        )

        if st.button(
            "Analyze food photo",
            type="primary",
            key="analyze_food_photo",
            width="content",
        ):
            try:
                service = FoodVisionService(
                    api_key=api_key,
                    model=self._get_vision_model(),
                )

                mime_type = getattr(
                    image_file,
                    "type",
                    None,
                ) or "image/jpeg"

                with st.spinner(
                    "Analyzing visible food and portions..."
                ):
                    analysis = service.analyze(
                        image_bytes=image_file.getvalue(),
                        mime_type=mime_type,
                    )

                st.session_state[
                    "food_photo_analysis"
                ] = analysis

            except Exception as exc:
                st.error(
                    f"Food analysis could not be completed: {exc}"
                )

        analysis = st.session_state.get(
            "food_photo_analysis"
        )

        if analysis is None:
            return

        st.subheader(
            "Estimated food analysis"
        )

        if analysis.items:
            items_frame = pd.DataFrame(
                analysis.items
            )
            st.dataframe(
                items_frame,
                width="stretch",
                hide_index=True,
            )

        metric_columns = st.columns(
            5
        )

        metric_columns[0].metric(
            "Calories",
            f"{analysis.calories:.0f}",
        )
        metric_columns[1].metric(
            "Protein",
            f"{analysis.protein_g:.1f} g",
        )
        metric_columns[2].metric(
            "Carbs",
            f"{analysis.carbs_g:.1f} g",
        )
        metric_columns[3].metric(
            "Fat",
            f"{analysis.fat_g:.1f} g",
        )
        metric_columns[4].metric(
            "Fiber",
            f"{analysis.fiber_g:.1f} g",
        )

        st.write(
            f"**Estimated quantity:** "
            f"{analysis.estimated_total_quantity}"
        )

        st.write(
            f"**Confidence:** "
            f"{analysis.confidence}"
        )

        if analysis.notes:
            st.caption(
                analysis.notes
            )

        st.subheader(
            "Save estimate"
        )

        save_col, meal_col = st.columns(
            2
        )

        recorded_on = save_col.date_input(
            "Date",
            date.today(),
            key="food_photo_save_date",
        )

        meal_type = meal_col.selectbox(
            "Meal type",
            [
                "Breakfast",
                "Lunch",
                "Dinner",
                "Snack",
            ],
            key="food_photo_meal_type",
        )

        if st.button(
            "Save estimated nutrition",
            key="save_food_photo_analysis",
            width="content",
        ):
            notes = (
                "AI food-photo estimate. "
                f"Items: {analysis.item_summary}. "
                f"Estimated quantity: "
                f"{analysis.estimated_total_quantity}. "
                f"Confidence: {analysis.confidence}. "
                f"{analysis.notes}"
            )

            self.repository.create(
                NutritionRecord(
                    client_id,
                    recorded_on,
                    meal_type,
                    analysis.calories,
                    analysis.protein_g,
                    analysis.carbs_g,
                    analysis.fat_g,
                    analysis.fiber_g,
                    0.0,
                    notes,
                ).to_dict()
            )

            st.session_state.pop(
                "food_photo_analysis",
                None,
            )

            st.success(
                "Estimated nutrition saved."
            )
            st.rerun()
