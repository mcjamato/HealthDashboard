from pathlib import Path

import streamlit as st

from config import (
    APP_ICON,
    APP_NAME,
    APP_VERSION,
    CSS_PATH,
    DATABASE_PATH,
)
from database.database import DatabaseManager
from imports.excel_importer import ExcelImporter
from pages.analytics_page import AnalyticsPage
from pages.clients_page import ClientsPage
from pages.customer_dashboard_page import CustomerDashboardPage
from pages.dashboard_page import DashboardPage
from pages.exercise_page import ExercisePage
from pages.health_page import HealthPage
from pages.import_page import ImportPage
from pages.mental_page import MentalWellnessPage
from pages.nutrition_page import NutritionPage
from pages.reports_page import ReportsPage
from pages.testing_page import TestingPage
from repositories.client_repository import ClientRepository
from repositories.domain_repository import (
    ExerciseRepository,
    HealthRepository,
    MentalWellnessRepository,
    NutritionRepository,
)
from repositories.report_repository import ReportRepository


st.set_page_config(
    page_title="Dashboard",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

if CSS_PATH.exists():
    st.markdown(
        f"<style>{CSS_PATH.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )

database = DatabaseManager(
    DATABASE_PATH,
    Path(__file__).parent / "database" / "schema.sql",
)
database.initialize()

clients = ClientRepository(database)
exercise = ExerciseRepository(database)
health = HealthRepository(database)
mental = MentalWellnessRepository(database)
nutrition = NutritionRepository(database)
report_repository = ReportRepository(database)

dashboard = DashboardPage(
    exercise,
    health,
    mental,
    nutrition,
)
analytics = AnalyticsPage(
    exercise,
    health,
    mental,
    nutrition,
)
customer_dashboards = CustomerDashboardPage(
    exercise,
    health,
    mental,
    nutrition,
)
importer = ExcelImporter(
    clients,
    exercise,
    health,
    mental,
    nutrition,
)
reports = ReportsPage(
    clients,
    exercise,
    health,
    mental,
    nutrition,
    report_repository,
)

NAVIGATION = {
    "Analyze": [
        "Dashboard",
        "Cross-Domain Analytics",
        "Reports",
    ],
    "Customer Dashboards": [
        "Exercise Dashboard",
        "Health Dashboard",
        "Mental Wellness Dashboard",
        "Nutrition Dashboard",
    ],
    "Customer Data": [
        "Client Profiles",
        "Exercise Entry",
        "Health Entry",
        "Mental Wellness Entry",
        "Nutrition Entry",
        "Excel Import",
        "Final Testing",
    ],
}


def render_sidebar() -> tuple[str, str, int | None]:
    """Render grouped navigation and customer context controls."""

    with st.sidebar:
        st.title("💙 Dashboard")
        st.caption(f"Health & Wellness · v{APP_VERSION}")

        st.markdown("### Navigation")

        category = st.selectbox(
            "Section",
            list(NAVIGATION.keys()),
            key="navigation_category",
        )

        page = st.radio(
            "Page",
            NAVIGATION[category],
            key=f"navigation_page_{category}",
        )

        st.divider()
        st.markdown("### Customer context")

        role_label = st.selectbox(
            "View as",
            ["Administrator", "Client"],
            key="role_selector",
        )
        role = (
            "admin"
            if role_label == "Administrator"
            else "client"
        )

        client_frame = clients.list_active()
        client_id = None

        if client_frame.empty:
            st.info(
                "No customers are registered yet. "
                "Open Customer Data → Client Profiles."
            )
        else:
            client_options = {
                (
                    f"{row.first_name} "
                    f"{row.last_name} "
                    f"(#{row.id})"
                ): int(row.id)
                for row in client_frame.itertuples()
            }

            selected_client = st.selectbox(
                "Customer",
                list(client_options.keys()),
                key="customer_selector",
            )
            client_id = client_options[selected_client]

        st.divider()
        st.caption(
            "Navigation chooses what to view. "
            "Customer context chooses whose data is displayed."
        )

    return page, role, client_id


page, role, client_id = render_sidebar()


if page == "Dashboard":
    dashboard.render(client_id)

elif page == "Cross-Domain Analytics":
    analytics.render(client_id)

elif page == "Reports":
    reports.render(client_id, role)

elif page == "Exercise Dashboard":
    customer_dashboards.render(
        domain="exercise",
        client_id=client_id,
    )

elif page == "Health Dashboard":
    customer_dashboards.render(
        domain="health",
        client_id=client_id,
    )

elif page == "Mental Wellness Dashboard":
    customer_dashboards.render(
        domain="mental",
        client_id=client_id,
    )

elif page == "Nutrition Dashboard":
    customer_dashboards.render(
        domain="nutrition",
        client_id=client_id,
    )

elif page == "Client Profiles":
    ClientsPage(clients).render(role)

elif page == "Exercise Entry":
    ExercisePage(exercise).render(
        client_id,
        role,
    )

elif page == "Health Entry":
    HealthPage(health).render(
        client_id,
        role,
    )

elif page == "Mental Wellness Entry":
    MentalWellnessPage(mental).render(
        client_id,
        role,
    )

elif page == "Nutrition Entry":
    NutritionPage(nutrition).render(
        client_id,
        role,
    )

elif page == "Excel Import":
    ImportPage(importer).render(role)

elif page == "Final Testing":
    TestingPage().render()
