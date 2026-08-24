from datetime import date

import streamlit as st


class ClientsPage:
    def __init__(self, repository) -> None:
        self.repository = repository

    def render(self, role: str) -> None:
        st.title("👥 Client Profiles")

        if role != "admin":
            st.info("Client profile management is available to administrators.")
            return

        with st.form("create_client", clear_on_submit=True):
            first, last = st.columns(2)
            first_name = first.text_input("First name")
            last_name = last.text_input("Last name")
            email = st.text_input("Email")
            birth_date = st.date_input(
                "Birth date",
                value=date(2000, 1, 1),
                min_value=date(1900, 1, 1),
                max_value=date.today(),
            )
            submitted = st.form_submit_button(
                "Create client", width="stretch"
            )

        if submitted:
            if not first_name.strip() or not last_name.strip() or not email.strip():
                st.error("First name, last name, and email are required.")
            else:
                try:
                    self.repository.create(
                        first_name,
                        last_name,
                        email,
                        birth_date.isoformat(),
                    )
                    st.success("Client created.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Client could not be created: {exc}")

        frame = self.repository.list_active()
        st.subheader("Active clients")
        st.dataframe(frame, width="stretch", hide_index=True)
