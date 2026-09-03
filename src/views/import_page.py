from pathlib import Path

import streamlit as st


class ImportPage:
    """Administrator import center for customer/intake and blood-work data."""

    CUSTOMER_ENTRIES = "Customer + Intake"
    BLOOD_WORK = "Blood Work"

    def __init__(self, customer_importer, blood_work_importer) -> None:
        self.customer_importer = customer_importer
        self.blood_work_importer = blood_work_importer

    def render(self, role: str) -> None:
        st.title("📥 Data Import")

        if role != "admin":
            st.warning("Data importing is available only to administrators.")
            return

        destination = st.selectbox(
            "Import destination",
            [self.CUSTOMER_ENTRIES, self.BLOOD_WORK],
            help=(
                "Customer + Intake imports the full intake questionnaire and can also "
                "import Exercise, Health, Mental Wellness, and Nutrition history from Excel. "
                "A CSV can be used for client intake-only imports."
            ),
            width=360,
        )

        if destination == self.CUSTOMER_ENTRIES:
            self._render_customer_import()
        else:
            self._render_blood_work_import()

    @staticmethod
    def _sample_file(name: str) -> Path:
        return Path(__file__).resolve().parents[2] / "sample_data" / name

    def _render_customer_import(self) -> None:
        st.subheader("Customer + Intake")
        st.write(
            "The Clients worksheet is based on the full Wellness Intake Questionnaire. "
            "Excel imports can also include Exercise, Health, MentalWellness, and Nutrition worksheets. "
            "Client email is the stable key used to match historical records."
        )

        template = self._sample_file("Wellness_Intake_Import_Template_v1.6.0.xlsx")
        if template.exists():
            template_bytes = template.read_bytes()
        else:
            template_bytes = self.customer_importer.template_bytes()

        st.download_button(
            label="Download intake + wellness Excel template",
            data=template_bytes,
            file_name="Wellness_Intake_Import_Template_v1.6.0.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width="content",
        )

        csv_template = self._sample_file("Wellness_Intake_Import_Template_v1.6.0.csv")
        if csv_template.exists():
            st.download_button(
                label="Download intake-only CSV template",
                data=csv_template.read_bytes(),
                file_name="Wellness_Intake_Import_Template_v1.6.0.csv",
                mime="text/csv",
                width="content",
            )

        uploaded = st.file_uploader(
            "Upload Excel workbook or intake CSV",
            type=["xlsx", "csv"],
            key="customer_entry_import_file",
            width="stretch",
        )

        if uploaded is not None and st.button(
            "Import customer/intake data",
            type="primary",
            key="import_customer_entries",
            width="content",
        ):
            with st.spinner("Importing customer/intake data..."):
                if uploaded.name.lower().endswith(".csv"):
                    result = self.customer_importer.import_clients_csv(uploaded.getvalue())
                else:
                    result = self.customer_importer.import_workbook(uploaded.getvalue())
            self._show_result(result)
            if result.imported > 0:
                st.rerun()

    def _render_blood_work_import(self) -> None:
        st.subheader("Blood Work")
        st.write(
            "Import laboratory results using a flexible test-name/value structure. "
            "Examples include glucose, A1C, LDL, HDL, hemoglobin, vitamin D, and others."
        )
        st.download_button(
            label="Download blood-work template",
            data=self.blood_work_importer.template_bytes(),
            file_name="blood_work_import_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            width="content",
        )
        uploaded = st.file_uploader(
            "Upload blood-work workbook", type=["xlsx"], key="blood_work_import_file", width="stretch"
        )
        if uploaded is not None and st.button(
            "Import blood work", type="primary", key="import_blood_work", width="content"
        ):
            with st.spinner("Importing blood work..."):
                result = self.blood_work_importer.import_workbook(uploaded.getvalue())
            self._show_result(result)

    @staticmethod
    def _show_result(result) -> None:
        if result.imported > 0:
            st.success(f"Imported rows: {result.imported}")
        if result.rejected > 0:
            st.warning(f"Rejected rows: {result.rejected}")
            with st.expander("Rejected-row details", expanded=True):
                for error in result.errors[:50]:
                    st.error(error)
        if result.imported == 0 and result.rejected == 0:
            st.info("No new rows were imported.")
