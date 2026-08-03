from pathlib import Path
import streamlit as st
from config import APP_ICON, APP_NAME, APP_VERSION, CSS_PATH, DATABASE_PATH
from database.database import DatabaseManager
from imports.excel_importer import ExcelImporter
from views.analytics_page import AnalyticsPage
from views.clients_page import ClientsPage
from views.dashboard_page import DashboardPage
from views.exercise_page import ExercisePage
from views.health_page import HealthPage
from views.import_page import ImportPage
from views.mental_page import MentalWellnessPage
from views.nutrition_page import NutritionPage
from views.reports_page import ReportsPage
from views.testing_page import TestingPage
from repositories.client_repository import ClientRepository
from repositories.domain_repository import ExerciseRepository, HealthRepository, MentalWellnessRepository, NutritionRepository
from repositories.report_repository import ReportRepository

st.set_page_config(page_title=APP_NAME, page_icon=APP_ICON, layout="wide")
if CSS_PATH.exists():
    st.markdown(f"<style>{CSS_PATH.read_text()}</style>", unsafe_allow_html=True)

db = DatabaseManager(DATABASE_PATH, Path(__file__).parent / "database" / "schema.sql")
db.initialize()
clients = ClientRepository(db)
exercise = ExerciseRepository(db)
health = HealthRepository(db)
mental = MentalWellnessRepository(db)
nutrition = NutritionRepository(db)
report_repository = ReportRepository(db)
dashboard = DashboardPage(exercise, health, mental, nutrition)
analytics = AnalyticsPage(exercise, health, mental, nutrition)
importer = ExcelImporter(clients, exercise, health, mental, nutrition)
reports = ReportsPage(clients, exercise, health, mental, nutrition, report_repository)

with st.sidebar:
    st.title("💙 Wellness")
    st.caption(f"Phase 4 - Version {APP_VERSION}")
    role = "admin" if st.selectbox("Demo role", ["Administrator", "Client"]) == "Administrator" else "client"
    frame = clients.list_active()
    client_id = None
    if not frame.empty:
        options = {f"{row.first_name} {row.last_name} (#{row.id})": int(row.id) for row in frame.itertuples()}
        client_id = options[st.selectbox("Selected client", list(options))]
    page = st.radio("Navigation", ["Dashboard", "Clients", "Exercise", "Health", "Mental Wellness", "Nutrition", "Cross-Domain Analytics", "Import Data", "Reports", "Final Testing"])

if page == "Dashboard": dashboard.render(client_id)
elif page == "Clients": ClientsPage(clients).render(role)
elif page == "Exercise": ExercisePage(exercise).render(client_id, role)
elif page == "Health": HealthPage(health).render(client_id, role)
elif page == "Mental Wellness": MentalWellnessPage(mental).render(client_id, role)
elif page == "Nutrition": NutritionPage(nutrition).render(client_id, role)
elif page == "Cross-Domain Analytics": analytics.render(client_id)
elif page == "Import Data": ImportPage(importer).render(role)
elif page == "Reports": reports.render(client_id, role)
else: TestingPage().render()
