import streamlit as st


class TestingPage:
    CHECKS = [
        "Login as administrator",
        "Create a client profile",
        "Create a client login",
        "Save each domain record",
        "Filter dashboard by month",
        "View customer dashboards",
        "Run correlation matrix",
        "Download Excel template",
        "Import valid workbook",
        "Reject malformed row",
        "Download client PDF",
        "Download administrator Excel",
        "Create report schedule",
        "Verify client role restrictions",
    ]

    def render(self) -> None:
        st.title("✅ Final Testing")
        for index, item in enumerate(self.CHECKS):
            st.checkbox(item, key=f"test_{index}")
