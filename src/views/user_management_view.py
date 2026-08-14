import streamlit as st


class UserManagementView:
    def __init__(self, users, clients, auth_service) -> None:
        self.users = users
        self.clients = clients
        self.auth_service = auth_service

    def render(self, role: str) -> None:
        st.title("🔐 User Accounts")

        if role != "admin":
            st.warning("Administrator only.")
            return

        client_frame = self.clients.list_active()

        if not client_frame.empty:
            options = {
                f"{row.first_name} {row.last_name} (#{row.id})": int(row.id)
                for row in client_frame.itertuples()
            }

            with st.form("create_client_login", clear_on_submit=True):
                selected_client = st.selectbox("Client", list(options.keys()))
                username = st.text_input("Username")
                password = st.text_input("Temporary password", type="password")
                create = st.form_submit_button(
                    "Create client login",
                    use_container_width=True,
                )

            if create:
                try:
                    self.users.create(
                        username=username,
                        password_hash=self.auth_service.hash_password(password),
                        role="client",
                        client_id=options[selected_client],
                    )
                    st.success("Client login created.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Account could not be created: {exc}")

        accounts = self.users.list_active()
        st.subheader("Active accounts")
        st.dataframe(accounts, use_container_width=True, hide_index=True)
