from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

import streamlit as st


class DashboardLayout:
    """Reusable Streamlit layout helpers for dashboard pages."""

    @staticmethod
    def render_client_header(
        client: dict[str, Any] | None,
        page_label: str,
    ) -> None:
        """Render a Streamlit-native client summary header."""

        st.title(page_label)

        with st.container(border=True):
            if client is None:
                left, right = st.columns(
                    [5, 1],
                    vertical_alignment="center",
                )

                with left:
                    st.caption("DASHBOARD PREVIEW")
                    st.subheader("No client selected")
                    st.write(
                        "Sample data is displayed until "
                        "a client is selected."
                    )

                with right:
                    st.info("Preview")

                return

            age_text = (
                str(client.get("age"))
                if client.get("age") is not None
                else "Not available"
            )

            name_column, status_column = st.columns(
                [5, 1],
                vertical_alignment="center",
            )

            with name_column:
                st.caption("VIEWING CLIENT")
                st.subheader(
                    str(
                        client.get(
                            "full_name",
                            "Unnamed client",
                        )
                    )
                )
                st.caption(
                    f"Client ID #{client.get('id', 'Unknown')}"
                )

            with status_column:
                st.success("Active")

            st.divider()

            age_column, email_column, birth_column = (
                st.columns(3)
            )

            with age_column:
                st.caption("Age")
                st.markdown(f"**{age_text}**")

            with email_column:
                st.caption("Email")
                st.markdown(
                    f"**{client.get('email', 'Not provided')}**"
                )

            with birth_column:
                st.caption("Birth date")
                st.markdown(
                    f"**{client.get('birth_date', 'Not provided')}**"
                )

    @staticmethod
    def render_filter_bar(
        render_filter: Callable[[], Any],
        title: str = "Dashboard filters",
        width_ratio: Sequence[int] = (1, 3),
    ) -> Any:
        """
        Render a compact left-aligned filter area.

        A 1:3 ratio keeps the filter near one quarter of the page width.
        """

        st.subheader(title)

        filter_column, _ = st.columns(
            list(width_ratio)
        )

        with filter_column:
            return render_filter()

    @staticmethod
    def render_kpi_row(
        metrics: Sequence[dict[str, Any]],
    ) -> None:
        """Render a row of metric cards."""

        if not metrics:
            return

        columns = st.columns(len(metrics))

        for column, metric in zip(
            columns,
            metrics,
            strict=True,
        ):
            with column:
                st.metric(
                    label=str(metric["label"]),
                    value=str(metric["value"]),
                    delta=metric.get("delta"),
                    help=metric.get("help"),
                    delta_color=metric.get(
                        "delta_color",
                        "normal",
                    ),
                )

    @staticmethod
    def render_chart_grid(
        charts: Sequence[
            tuple[str, Any, dict[str, Any] | None]
        ],
        columns_per_row: int = 2,
    ) -> None:
        """
        Render Plotly charts in a consistent responsive grid.

        Each chart tuple contains:
        (title, figure, optional Plotly config)
        """

        if not charts:
            return

        for start in range(
            0,
            len(charts),
            columns_per_row,
        ):
            row_items = charts[
                start:start + columns_per_row
            ]
            columns = st.columns(
                columns_per_row
            )

            for index, (
                title,
                figure,
                config,
            ) in enumerate(row_items):
                with columns[index]:
                    if title:
                        st.markdown(f"#### {title}")

                    st.plotly_chart(
                        figure,
                        use_container_width=True,
                        config=config or {},
                    )

    @staticmethod
    def render_section_title(
        title: str,
        caption: str | None = None,
    ) -> None:
        """Render a consistent dashboard section heading."""

        st.subheader(title)

        if caption:
            st.caption(caption)
