import pandas as pd
import plotly.express as px
import streamlit as st

from services.correlation_service import CorrelationService


class AnalyticsPage:
    def __init__(self, exercise, health, mental, nutrition) -> None:
        self.exercise = exercise
        self.health = health
        self.mental = mental
        self.nutrition = nutrition
        self.correlations = CorrelationService()

    def render(self, client_id: int | None) -> None:
        st.title("🔗 Cross-Domain Analytics")
        st.caption("Correlation describes association; it does not prove causation.")

        if client_id is None:
            st.info("Select a client to run correlations.")
            return

        daily = self.correlations.build_daily_dataset(
            self.exercise.list_for_client(client_id),
            self.health.list_for_client(client_id),
            self.mental.list_for_client(client_id),
            self.nutrition.list_for_client(client_id),
        )

        if len(daily) < 2:
            st.warning("At least two matching dates are required.")
            return

        st.dataframe(daily, use_container_width=True, hide_index=True)

        matrix = self.correlations.correlation_matrix(daily)
        if matrix.empty:
            st.warning("More repeated measurements are required.")
            return

        st.plotly_chart(
            px.imshow(
                matrix,
                text_auto=".2f",
                zmin=-1,
                zmax=1,
                aspect="auto",
                title="Pearson correlation matrix",
            ),
            use_container_width=True,
        )
