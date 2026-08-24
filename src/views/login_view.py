import streamlit as st

from auth.session_manager import SessionManager


class LoginView:
    def __init__(self, auth_service) -> None:
        self.auth_service = auth_service

    def render(self) -> None:
        _, center, _ = st.columns([1.2, 1, 1.2])

        with center:
            with st.container(border=True):
                st.title("💙 Wellness")
                st.caption("Health & Wellness Analytics Dashboard")

                with st.form("login_form"):
                    username = st.text_input(
                        "Username",
                        placeholder="Enter username",
                    )
                    password = st.text_input(
                        "Password",
                        type="password",
                        placeholder="Enter password",
                    )
                    submitted = st.form_submit_button(
                        "Sign in",
                        width="stretch",
                        type="primary",
                    )

                if submitted:
                    user = self.auth_service.authenticate(username, password)
                    if user is None:
                        st.error("Invalid username or password.")
                    else:
                        SessionManager.login(user)
                        st.rerun()
