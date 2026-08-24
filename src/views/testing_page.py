import streamlit as st


class TestingPage:
    CHECKS = [
        "Login as administrator",
        "Create or import client profiles",
        "Create a client login linked to one client",
        "Login as that client",
        "Verify client cannot select another customer",
        "Verify client does not see Analyze navigation",
        "Verify client sees Customer Dashboards",
        "Verify client sees Exercise Entry",
        "Verify client sees Health Entry",
        "Verify client sees Mental Wellness Entry",
        "Verify client sees Nutrition Entry",
        "Verify client sees Blood Work",
        "Verify client sees Change Password",
        "Verify client does not see Client Profiles",
        "Verify client does not see User Accounts",
        "Verify client does not see Data Import",
        "Verify client does not see Final Testing",
        "Enter client wellness data",
        "View client progress charts",
        "Download chart CSV",
        "Download chart PNG from Plotly camera icon",
        "Change administrator password",
        "Change client password",
        "Import customer-entry workbook",
        "Import blood-work workbook",
        "Use food-photo analyzer when API secret is configured",
    ]

    def render(
        self,
    ) -> None:
        st.title(
            "✅ Final Testing"
        )

        st.caption(
            "Administrator-only acceptance checklist."
        )

        for index, item in enumerate(
            self.CHECKS
        ):
            st.checkbox(
                item,
                key=f"test_{index}",
            )
