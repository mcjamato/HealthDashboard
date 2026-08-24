import streamlit as st


class ChangePasswordView:
    """Allows any authenticated user to change their own password."""

    def __init__(
        self,
        auth_service,
    ) -> None:
        self.auth_service = auth_service

    def render(
        self,
        current_user: dict,
    ) -> None:
        st.title(
            "🔑 Change Password"
        )

        st.caption(
            f"Signed in as {current_user['username']}"
        )

        with st.form(
            "change_password_form"
        ):
            current_password = st.text_input(
                "Current password",
                type="password",
            )

            new_password = st.text_input(
                "New password",
                type="password",
                help="Minimum 8 characters.",
            )

            confirm_password = st.text_input(
                "Confirm new password",
                type="password",
            )

            submitted = st.form_submit_button(
                "Change password",
                width="stretch",
                type="primary",
            )

        if submitted:
            try:
                self.auth_service.change_password(
                    user_id=int(
                        current_user["user_id"]
                    ),
                    current_password=current_password,
                    new_password=new_password,
                    confirm_password=confirm_password,
                )

                st.success(
                    "Password changed successfully."
                )

            except ValueError as exc:
                st.error(
                    str(exc)
                )
