from __future__ import annotations

from typing import Any

import streamlit as st


class ClientHeader:
    """Renders a Streamlit-native client summary header."""

    @staticmethod
    def render(
        client: dict[str, Any] | None,
        page_label: str,
    ) -> None:
        """Display the page title and selected-client context."""

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
