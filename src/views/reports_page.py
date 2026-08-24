from datetime import date

import streamlit as st

from reports.export_service import ExcelExportService
from reports.pdf_generator import PDFReportGenerator
from services.correlation_service import CorrelationService


class ReportsPage:
    def __init__(self, clients, exercise, health, mental, nutrition, reports) -> None:
        self.clients = clients
        self.exercise = exercise
        self.health = health
        self.mental = mental
        self.nutrition = nutrition
        self.reports = reports
        self.pdf = PDFReportGenerator()
        self.excel = ExcelExportService()
        self.corr = CorrelationService()

    def render(self, client_id: int | None, role: str) -> None:
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

        e = self.exercise.list_for_client(client_id)
        h = self.health.list_for_client(client_id)
        m = self.mental.list_for_client(client_id)
        n = self.nutrition.list_for_client(client_id)

        matrix = self.corr.correlation_matrix(
            self.corr.build_daily_dataset(e, h, m, n)
        )

        pdf_bytes = self.pdf.create(
            name,
            [
                ("Exercise", e),
                ("Health", h),
                ("Mental Wellness", m),
                ("Nutrition", n),
            ],
            matrix,
        )

        st.download_button(
            "Download client PDF report",
            pdf_bytes,
            f"{name.replace(' ', '_')}_wellness_report.pdf",
            "application/pdf",
            width="stretch",
        )

        if role == "admin":
            excel_bytes = self.excel.client_workbook(
                client, e, h, m, n, matrix
            )
            st.download_button(
                "Download administrator Excel report",
                excel_bytes,
                f"{name.replace(' ', '_')}_wellness_report.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                width="stretch",
            )

            st.subheader("Schedule a report")
            with st.form("schedule_report"):
                report_type = st.selectbox(
                    "Report type",
                    [
                        "Complete wellness",
                        "Exercise",
                        "Health",
                        "Mental Wellness",
                        "Nutrition",
                    ],
                )
                frequency = st.selectbox(
                    "Frequency",
                    ["Weekly", "Monthly", "Quarterly", "Annually"],
                )
                next_run = st.date_input("Next run date", date.today())
                output_format = st.selectbox(
                    "Output format",
                    ["PDF", "PDF and Excel"],
                )
                submitted = st.form_submit_button("Save schedule")

            if submitted:
                self.reports.create_schedule(
                    client_id,
                    report_type,
                    frequency,
                    next_run.isoformat(),
                    output_format,
                )
                st.rerun()

            schedules = self.reports.list_active_schedules()
            st.dataframe(
                schedules,
                width="stretch",
                hide_index=True,
            )
