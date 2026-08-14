import pandas as pd
import streamlit as st


class PageSupport:
    @staticmethod
    def require_client(client_id: int | None) -> bool:
        if client_id is None:
            st.info("Select a client before entering wellness data.")
            return False
        return True

    @staticmethod
    def show_history(frame: pd.DataFrame, title: str) -> None:
        st.subheader(title)
        if frame.empty:
            st.caption("No records have been entered yet.")
            return
        st.dataframe(
            frame.drop(columns=["is_active"], errors="ignore"),
            use_container_width=True,
            hide_index=True,
        )

    @staticmethod
    def admin_deactivate(repository, frame, key: str) -> None:
        if frame.empty:
            return
        with st.expander("Administrator record controls"):
            record_id = st.selectbox(
                "Record to deactivate",
                frame["id"].astype(int).tolist(),
                key=f"{key}_deactivate_id",
            )
            if st.button(
                "Deactivate selected record",
                key=f"{key}_deactivate_button",
            ):
                repository.deactivate(int(record_id))
                st.success("Record deactivated.")
                st.rerun()
