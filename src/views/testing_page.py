import streamlit as st


class TestingPage:
    CHECKS = [
        "Login as administrator",
        "Create or import a client profile",
        "Create a client login",
        "Change administrator password",
        "Change client password",
        "Save each wellness-domain record",
        "Filter dashboard by month",
        "Download chart CSV",
        "Download chart PNG from Plotly camera icon",
        "View customer dashboards",
        "Run correlation matrix",
        "Import customer-entry workbook",
        "Import blood-work workbook",
        "View blood-work trend",
        "Use food-photo analyzer when API secret is configured",
        "Download client PDF",
        "Download administrator Excel",
        "Create report schedule",
        "Verify client role restrictions",
    ]

    def render(
        self,
    ) -> None:
        st.title(
            "✅ Final Testing"
        )

        for index, item in enumerate(
            self.CHECKS
        ):
            st.checkbox(
                item,
                key=f"test_{index}",
            )
