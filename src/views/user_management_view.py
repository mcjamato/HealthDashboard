import streamlit as st


class UserManagementView:
    """Administrator user-account management and password reset."""

    def __init__(
        self,
        users,
        clients,
        auth_service,
    ) -> None:
        self.users = users
        self.clients = clients
        self.auth_service = auth_service

    def render(
        self,
        role: str,
    ) -> None:
        st.title(
            "🔐 User Accounts"
        )

        if role != "admin":
            st.warning(
                "Administrator only."
            )
            return

        client_frame = self.clients.list_active()

        st.subheader(
            "Create client login"
        )

        if client_frame.empty:
            st.info(
                "Create or import clients before "
                "creating client logins."
            )
        else:
            options = {
                (
                    f"{row.first_name} "
                    f"{row.last_name} "
                    f"(#{row.id})"
                ): int(row.id)
                for row
                in client_frame.itertuples()
            }

            with st.form(
                "create_client_login",
                clear_on_submit=True,
            ):
                selected_client = st.selectbox(
                    "Client",
                    list(
                        options.keys()
                    ),
                )

                username = st.text_input(
                    "Username"
                )

                password = st.text_input(
                    "Temporary password",
                    type="password",
                )

                create = st.form_submit_button(
                    "Create client login",
                    width="stretch",
                )

            if create:
                try:
                    self.users.create(
                        username=username,
                        password_hash=(
                            self.auth_service
                            .hash_password(
                                password
                            )
                        ),
                        role="client",
                        client_id=options[
                            selected_client
                        ],
                    )

                    st.success(
                        "Client login created."
                    )
                    st.rerun()

                except Exception as exc:
                    st.error(
                        f"Account could not be created: {exc}"
                    )

        accounts = self.users.list_active()

        st.subheader(
            "Active accounts"
        )

        st.dataframe(
            accounts,
            width="stretch",
            hide_index=True,
        )

        if accounts.empty:
            return

        st.subheader(
            "Administrator password reset"
        )

        account_options = {
            (
                f"{row.username} "
                f"({row.role}) "
                f"- {row.client}"
            ): int(row.id)
            for row
            in accounts.itertuples()
        }

        with st.form(
            "admin_password_reset"
        ):
            selected_account = st.selectbox(
                "Account",
                list(
                    account_options.keys()
                ),
            )

            new_password = st.text_input(
                "New temporary password",
                type="password",
                help="Minimum 8 characters.",
            )

            reset = st.form_submit_button(
                "Reset password",
                width="stretch",
            )

        if reset:
            try:
                self.auth_service.reset_password(
                    user_id=account_options[
                        selected_account
                    ],
                    new_password=new_password,
                )

                st.success(
                    "Password reset successfully."
                )

            except ValueError as exc:
                st.error(
                    str(exc)
                )
