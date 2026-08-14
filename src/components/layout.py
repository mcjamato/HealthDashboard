from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

import streamlit as st


class DashboardLayout:
    @staticmethod
    def render_client_header(client: dict | None, page_label: str) -> None:
        st.title(page_label)

        with st.container(border=True):
            if client is None:
                left, right = st.columns([5, 1], vertical_alignment="center")
                with left:
                    st.caption("DASHBOARD PREVIEW")
                    st.subheader("No client selected")
                    st.write("Sample data is displayed until a client is selected.")
                with right:
                    st.info("Preview")
                return

            name_col, status_col = st.columns([5, 1], vertical_alignment="center")
            with name_col:
                st.caption("VIEWING CLIENT")
                st.subheader(str(client.get("full_name", "Unnamed client")))
                st.caption(f"Client ID #{client.get('id', 'Unknown')}")
            with status_col:
                st.success("Active")

            st.divider()
            age_col, email_col, birth_col = st.columns(3)
            with age_col:
                st.caption("Age")
                st.markdown(
                    f"**{client.get('age') if client.get('age') is not None else 'Not available'}**"
                )
            with email_col:
                st.caption("Email")
                st.markdown(f"**{client.get('email', 'Not provided')}**")
            with birth_col:
                st.caption("Birth date")
                st.markdown(f"**{client.get('birth_date', 'Not provided')}**")

    @staticmethod
    def render_filter_bar(
        render_filter: Callable[[], Any],
        title: str = "Dashboard filters",
        width_ratio: Sequence[int] = (1, 4),
    ) -> Any:
        st.subheader(title)
        filter_column, _ = st.columns(list(width_ratio))
        with filter_column:
            return render_filter()

    @staticmethod
    def render_kpi_row(metrics: Sequence[dict[str, Any]]) -> None:
        if not metrics:
            return
        columns = st.columns(len(metrics))
        for column, metric in zip(columns, metrics):
            with column:
                st.metric(
                    label=str(metric["label"]),
                    value=str(metric["value"]),
                    delta=metric.get("delta"),
                    help=metric.get("help"),
                    delta_color=metric.get("delta_color", "normal"),
                )

    @staticmethod
    def render_chart_grid(charts, columns_per_row: int = 2) -> None:
        for start in range(0, len(charts), columns_per_row):
            row_items = charts[start:start + columns_per_row]
            columns = st.columns(columns_per_row)
            for index, (title, figure, config) in enumerate(row_items):
                with columns[index]:
                    if title:
                        st.markdown(f"#### {title}")
                    st.plotly_chart(
                        figure,
                        use_container_width=True,
                        config=config or {},
                    )
