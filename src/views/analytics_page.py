import plotly.express as px
import streamlit as st

from components.layout import DashboardLayout
from services.correlation_service import CorrelationService


class AnalyticsPage:
    """Cross-domain correlation analytics with export controls."""

    def __init__(
        self,
        exercise,
        health,
        mental,
        nutrition,
    ) -> None:
        self.exercise = exercise
        self.health = health
        self.mental = mental
        self.nutrition = nutrition
        self.correlations = (
            CorrelationService()
        )

    def render(
        self,
        client_id: int | None,
    ) -> None:
        st.title(
            "🔗 Cross-Domain Analytics"
        )

        st.caption(
            "Correlation describes association; "
            "it does not prove causation."
        )

        if client_id is None:
            st.info(
                "Select a client to run correlations."
            )
            return

        daily = (
            self.correlations
            .build_daily_dataset(
                self.exercise.list_for_client(
                    client_id
                ),
                self.health.list_for_client(
                    client_id
                ),
                self.mental.list_for_client(
                    client_id
                ),
                self.nutrition.list_for_client(
                    client_id
                ),
            )
        )

        if len(
            daily
        ) < 2:
            st.warning(
                "At least two matching dates are required."
            )
            return

        matrix = (
            self.correlations
            .correlation_matrix(
                daily
            )
        )

        if matrix.empty:
            st.warning(
                "More repeated measurements are required."
            )
            return

        figure = px.imshow(
            matrix,
            text_auto=".2f",
            zmin=-1,
            zmax=1,
            aspect="auto",
            title=(
                "Pearson correlation matrix"
            ),
        )

        matrix_export = (
            matrix.reset_index()
            .rename(
                columns={
                    "index": "metric"
                }
            )
        )

        DashboardLayout.render_exportable_chart(
            title="Correlation matrix",
            figure=figure,
            data=matrix_export,
            filename="correlation_matrix",
            key="correlation_matrix",
        )

        st.subheader(
            "Combined daily dataset"
        )

        st.dataframe(
            daily,
            width="stretch",
            hide_index=True,
        )

        st.download_button(
            "Download combined daily CSV",
            data=daily.to_csv(
                index=False
            ).encode(
                "utf-8"
            ),
            file_name=(
                "cross_domain_daily_data.csv"
            ),
            mime="text/csv",
            width="content",
        )
