from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from components.layout import DashboardLayout
from views.shared import PageSupport


class BloodWorkPage:
    """Manual entry, history, and trends for laboratory results."""

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
            "🧪 Blood Work"
        )

        if not PageSupport.require_client(
            client_id
        ):
            return

        with st.form(
            "blood_work_form",
            clear_on_submit=True,
        ):
            recorded_on = st.date_input(
                "Test date",
                date.today(),
            )

            test_name = st.text_input(
                "Test name",
                placeholder="Example: LDL Cholesterol",
            )

            value = st.number_input(
                "Value",
                value=0.0,
                step=0.1,
            )

            unit = st.text_input(
                "Unit",
                placeholder="Example: mg/dL",
            )

            low_col, high_col = st.columns(
                2
            )

            reference_low = low_col.number_input(
                "Reference low",
                value=None,
                step=0.1,
            )

            reference_high = high_col.number_input(
                "Reference high",
                value=None,
                step=0.1,
            )

            notes = st.text_area(
                "Notes"
            )

            submitted = st.form_submit_button(
                "Save blood-work result",
                width="stretch",
            )

        if submitted:
            if not test_name.strip():
                st.error(
                    "Test name is required."
                )
            else:
                self.repository.create(
                    {
                        "client_id": int(
                            client_id
                        ),
                        "recorded_on": (
                            recorded_on.isoformat()
                        ),
                        "test_name": test_name.strip(),
                        "value": float(value),
                        "unit": unit.strip(),
                        "reference_low": reference_low,
                        "reference_high": reference_high,
                        "notes": notes.strip(),
                    }
                )

                st.success(
                    "Blood-work result saved."
                )
                st.rerun()

        frame = self.repository.list_for_client(
            int(client_id)
        )

        if frame.empty:
            st.info(
                "No blood-work results are available yet."
            )
            return

        st.subheader(
            "Blood-work trends"
        )

        tests = sorted(
            frame["test_name"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_test = st.selectbox(
            "Test",
            tests,
            width=360,
        )

        test_data = frame[
            frame["test_name"]
            == selected_test
        ].copy()

        test_data["recorded_on"] = pd.to_datetime(
            test_data["recorded_on"],
            errors="coerce",
        )

        test_data = test_data.sort_values(
            "recorded_on"
        )

        figure = px.line(
            test_data,
            x="recorded_on",
            y="value",
            markers=True,
        )

        figure.update_traces(
            hovertemplate=(
                "<b>%{x|%B %d, %Y}</b><br>"
                "Value: %{y}<extra></extra>"
            )
        )

        DashboardLayout.render_exportable_chart(
            title=f"{selected_test} trend",
            figure=figure,
            data=test_data,
            filename=(
                f"blood_work_{selected_test}"
            ),
            key="blood_work_trend",
        )

        PageSupport.show_history(
            frame,
            "Blood-work history",
        )

        if role == "admin":
            PageSupport.admin_deactivate(
                self.repository,
                frame,
                "blood_work",
            )
