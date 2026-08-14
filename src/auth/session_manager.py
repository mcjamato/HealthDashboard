from __future__ import annotations

import streamlit as st


class SessionManager:
    AUTH_KEY = "wellness_authenticated"
    USER_KEY = "wellness_user"

    @staticmethod
    def is_authenticated() -> bool:
        return bool(st.session_state.get(SessionManager.AUTH_KEY, False))

    @staticmethod
    def login(user: dict) -> None:
        st.session_state[SessionManager.AUTH_KEY] = True
        st.session_state[SessionManager.USER_KEY] = user

    @staticmethod
    def current_user() -> dict | None:
        return st.session_state.get(SessionManager.USER_KEY)

    @staticmethod
    def logout() -> None:
        st.session_state.pop(SessionManager.AUTH_KEY, None)
        st.session_state.pop(SessionManager.USER_KEY, None)
