from datetime import date

import streamlit as st

from components.intake_form import IntakeForm


class ClientsPage:
    def __init__(self, repository, intake_repository) -> None:
        self.repository = repository
        self.intake_repository = intake_repository

    def render(self, role: str) -> None:
        st.title("👥 Client Profiles")

        if role != "admin":
            st.info("Client profile management is available to administrators.")
            return

        st.caption(
            "Create a client manually using the same fields as the Wellness Intake Questionnaire. "
            "Only name and email are required; the remaining intake sections can be completed now or later."
        )

        with st.form("create_client", clear_on_submit=False):
            st.subheader("Client identity")
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

            st.subheader("Wellness intake questionnaire")
            intake_values = IntakeForm.render_fields(key_prefix="new_client_intake")
            submitted = st.form_submit_button("Create client", width="stretch")

        if submitted:
            if not first_name.strip() or not last_name.strip() or not email.strip():
                st.error("First name, last name, and email are required.")
            else:
                try:
                    client_id = self.repository.create(
                        first_name,
                        last_name,
                        email,
                        birth_date.isoformat(),
                    )
                    self.intake_repository.upsert(client_id, intake_values)
                    st.success("Client and intake profile created.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Client could not be created: {exc}")

        frame = self.repository.list_active()
        st.subheader("Active clients")
        st.dataframe(frame, width="stretch", hide_index=True)
