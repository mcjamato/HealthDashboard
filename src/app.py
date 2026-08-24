from pathlib import Path
import os

import streamlit as st

from auth.auth_service import AuthService
from auth.session_manager import SessionManager
from components.navigation import RoleNavigation
from config import (
    APP_ICON,
    APP_VERSION,
    CSS_PATH,
    DATABASE_PATH,
)
from database.database import DatabaseManager
from imports.blood_work_importer import BloodWorkImporter
from imports.excel_importer import ExcelImporter
from repositories.client_repository import ClientRepository
from repositories.domain_repository import (
    BloodWorkRepository,
    ExerciseRepository,
    HealthRepository,
    MentalWellnessRepository,
    NutritionRepository,
)
from repositories.report_repository import ReportRepository
from repositories.user_repository import UserRepository
from utilities.client_context import ClientContext
from views.analytics_page import AnalyticsPage
from views.blood_work_page import BloodWorkPage
from views.change_password_view import ChangePasswordView
from views.clients_page import ClientsPage
from views.customer_dashboard_page import CustomerDashboardPage
from views.dashboard_page import DashboardPage
from views.exercise_page import ExercisePage
from views.health_page import HealthPage
from views.import_page import ImportPage
from views.login_view import LoginView
from views.mental_page import MentalWellnessPage
from views.nutrition_page import NutritionPage
from views.reports_page import ReportsPage
from views.testing_page import TestingPage
from views.user_management_view import UserManagementView


st.set_page_config(
    page_title="Dashboard",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

if CSS_PATH.exists():
    st.markdown(
        (
            "<style>"
            f"{CSS_PATH.read_text(encoding='utf-8')}"
            "</style>"
        ),
        unsafe_allow_html=True,
    )

database = DatabaseManager(
    DATABASE_PATH,
    (
        Path(__file__).parent
        / "database"
        / "schema.sql"
    ),
)
database.initialize()

clients = ClientRepository(
    database
)
users = UserRepository(
    database
)
exercise = ExerciseRepository(
    database
)
health = HealthRepository(
    database
)
mental = MentalWellnessRepository(
    database
)
nutrition = NutritionRepository(
    database
)
blood_work = BloodWorkRepository(
    database
)
report_repository = ReportRepository(
    database
)

auth_service = AuthService(
    users
)

created = auth_service.ensure_initial_admin(
    username=os.getenv(
        "WELLNESS_ADMIN_USERNAME",
        "admin",
    ),
    password=os.getenv(
        "WELLNESS_ADMIN_PASSWORD",
        "ChangeMe123!",
    ),
)

if not SessionManager.is_authenticated():
    LoginView(
        auth_service
    ).render()

    if created:
        st.info(
            "First-run admin created. "
            "Default username: admin"
        )

    st.stop()

current_user = SessionManager.current_user()

if current_user is None:
    SessionManager.logout()
    st.rerun()

role = current_user[
    "role"
]

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

customer_importer = ExcelImporter(
    clients,
    exercise,
    health,
    mental,
    nutrition,
)

blood_work_importer = BloodWorkImporter(
    clients,
    blood_work,
)

reports = ReportsPage(
    clients,
    exercise,
    health,
    mental,
    nutrition,
    report_repository,
)

user_management = UserManagementView(
    users,
    clients,
    auth_service,
)

change_password = ChangePasswordView(
    auth_service
)

navigation = RoleNavigation.for_role(
    role
)

with st.sidebar:
    st.title(
        "💙 Dashboard"
    )

    st.caption(
        f"Health & Wellness · "
        f"v{APP_VERSION}"
    )

    role_label = (
        "Administrator"
        if role == "admin"
        else "Client"
    )

    st.caption(
        f"Signed in as "
        f"{current_user['username']} "
        f"· {role_label}"
    )

    category = st.selectbox(
        "Section",
        list(
            navigation.keys()
        ),
        key="navigation_category",
    )

    page = st.radio(
        "Page",
        navigation[
            category
        ],
        key=(
            f"navigation_page_"
            f"{role}_"
            f"{category}"
        ),
    )

    st.divider()

    st.markdown(
        "### Customer context"
    )

    client_frame = clients.list_active()

    client_id = None
    client_context = None

    if role == "client":
        # Client accounts are permanently tied to their own client_id.
        # No customer selector is rendered for client users.
        client_id = current_user[
            "client_id"
        ]

        if client_id is None:
            st.error(
                "This client login is not linked "
                "to a client profile. "
                "Contact the administrator."
            )
        elif client_frame.empty:
            st.error(
                "The linked client profile is not available."
            )
        else:
            match = client_frame[
                client_frame["id"]
                == client_id
            ]

            if match.empty:
                st.error(
                    "The linked client profile is inactive "
                    "or no longer available. "
                    "Contact the administrator."
                )
            else:
                client_context = ClientContext.from_row(
                    match.iloc[
                        0
                    ].to_dict()
                )

                st.success(
                    client_context[
                        "full_name"
                    ]
                )

                st.caption(
                    "You can enter new wellness data "
                    "and view your own progress dashboards."
                )

    else:
        if client_frame.empty:
            st.info(
                "Create or import a client "
                "profile to begin."
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

            selected = st.selectbox(
                "Customer",
                list(
                    options.keys()
                ),
                key="customer_selector",
            )

            client_id = options[
                selected
            ]

            match = client_frame[
                client_frame["id"]
                == client_id
            ]

            if not match.empty:
                client_context = ClientContext.from_row(
                    match.iloc[
                        0
                    ].to_dict()
                )

    st.divider()

    if st.button(
        "Log out",
        width="stretch",
    ):
        SessionManager.logout()
        st.rerun()


# A second authorization check protects against a stale or manipulated
# Streamlit session navigating to a page outside the role menu.
if not RoleNavigation.is_allowed(
    role,
    page,
):
    st.error(
        "You do not have permission "
        "to access this page."
    )
    st.stop()


if page == "Dashboard":
    dashboard.render(
        client_id,
        client_context,
    )

elif page == "Cross-Domain Analytics":
    analytics.render(
        client_id
    )

elif page == "Reports":
    reports.render(
        client_id,
        role,
    )

elif page == "Exercise Dashboard":
    customer_dashboards.render(
        "exercise",
        client_id,
        client_context,
    )

elif page == "Health Dashboard":
    customer_dashboards.render(
        "health",
        client_id,
        client_context,
    )

elif page == "Mental Wellness Dashboard":
    customer_dashboards.render(
        "mental",
        client_id,
        client_context,
    )

elif page == "Nutrition Dashboard":
    customer_dashboards.render(
        "nutrition",
        client_id,
        client_context,
    )

elif page == "Client Profiles":
    ClientsPage(
        clients
    ).render(
        role
    )

elif page == "User Accounts":
    user_management.render(
        role
    )

elif page == "Exercise Entry":
    ExercisePage(
        exercise
    ).render(
        client_id,
        role,
    )

elif page == "Health Entry":
    HealthPage(
        health
    ).render(
        client_id,
        role,
    )

elif page == "Mental Wellness Entry":
    MentalWellnessPage(
        mental
    ).render(
        client_id,
        role,
    )

elif page == "Nutrition Entry":
    NutritionPage(
        nutrition
    ).render(
        client_id,
        role,
    )

elif page == "Blood Work":
    BloodWorkPage(
        blood_work
    ).render(
        client_id,
        role,
    )

elif page == "Data Import":
    ImportPage(
        customer_importer,
        blood_work_importer,
    ).render(
        role
    )

elif page == "Change Password":
    change_password.render(
        current_user
    )

elif page == "Final Testing":
    TestingPage().render()
