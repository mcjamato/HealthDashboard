from datetime import date
import streamlit as st
from reports.export_service import ExcelExportService
from reports.pdf_generator import PDFReportGenerator
from services.correlation_service import CorrelationService

class ReportsPage:
    def __init__(self, clients, exercise, health, mental, nutrition, reports):
        self.clients = clients
        self.exercise = exercise
        self.health = health
        self.mental = mental
        self.nutrition = nutrition
        self.reports = reports
        self.pdf = PDFReportGenerator()
        self.excel = ExcelExportService()
        self.correlation = CorrelationService()

    def render(self, client_id, role):
        st.title("📄 Reports")
        if client_id is None:
            st.info("Select a client.")
            return
        clients = self.clients.list_active()
        match = clients[clients["id"] == client_id]
        if match.empty:
            st.error("Client not found.")
            return
        client = match.iloc[0].to_dict()
        name = f"{client['first_name']} {client['last_name']}"
        exercise = self.exercise.list_for_client(client_id)
        health = self.health.list_for_client(client_id)
        mental = self.mental.list_for_client(client_id)
        nutrition = self.nutrition.list_for_client(client_id)
        matrix = self.correlation.correlation_matrix(self.correlation.build_daily_dataset(exercise, health, mental, nutrition))
        pdf = self.pdf.create(name, [("Exercise", exercise), ("Health", health), ("Mental Wellness", mental), ("Nutrition", nutrition)], matrix)
        st.download_button("Download client PDF report", pdf, f"{name.replace(' ', '_')}_wellness_report.pdf", "application/pdf", use_container_width=True)
        if role == "admin":
            xlsx = self.excel.client_workbook(client, exercise, health, mental, nutrition, matrix)
            st.download_button("Download administrator Excel report", xlsx, f"{name.replace(' ', '_')}_wellness_report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
            with st.form("schedule"):
                report_type = st.selectbox("Report type", ["Complete wellness", "Exercise", "Health", "Mental Wellness", "Nutrition"])
                frequency = st.selectbox("Frequency", ["Weekly", "Monthly", "Quarterly", "Annually"])
                next_run = st.date_input("Next run date", date.today())
                output_format = st.selectbox("Output format", ["PDF", "PDF and Excel"])
                submitted = st.form_submit_button("Save schedule")
            if submitted:
                self.reports.create_schedule(client_id, report_type, frequency, next_run.isoformat(), output_format)
                st.rerun()
            schedules = self.reports.list_active_schedules()
            st.dataframe(schedules, use_container_width=True, hide_index=True)
            if not schedules.empty:
                schedule_id = st.selectbox("Schedule to deactivate", schedules["id"].astype(int).tolist())
                if st.button("Deactivate schedule"):
                    self.reports.deactivate_schedule(int(schedule_id))
                    st.rerun()
