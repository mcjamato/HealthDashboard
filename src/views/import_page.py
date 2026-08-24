import streamlit as st


class ImportPage:
    """Administrator import center for customer and blood-work data."""

    CUSTOMER_ENTRIES = "Customer Entries"
    BLOOD_WORK = "Blood Work"

    def __init__(
        self,
        customer_importer,
        blood_work_importer,
    ) -> None:
        self.customer_importer = (
            customer_importer
        )
        self.blood_work_importer = (
            blood_work_importer
        )

    def render(
        self,
        role: str,
    ) -> None:
        st.title(
            "📥 Data Import"
        )

        if role != "admin":
            st.warning(
                "Data importing is available "
                "only to administrators."
            )
            return

        destination = st.selectbox(
            "Import destination",
            [
                self.CUSTOMER_ENTRIES,
                self.BLOOD_WORK,
            ],
            help=(
                "Customer Entries imports client profiles "
                "plus Exercise, Health, Mental Wellness, "
                "and Nutrition data. Blood Work imports "
                "laboratory results."
            ),
            width=360,
        )

        if destination == self.CUSTOMER_ENTRIES:
            self._render_customer_import()
        else:
            self._render_blood_work_import()

    def _render_customer_import(
        self,
    ) -> None:
        st.subheader(
            "Customer Entries"
        )

        st.write(
            "Imports Clients, Exercise, Health, "
            "MentalWellness, and Nutrition worksheets. "
            "Client email is used to match each record "
            "to the correct customer."
        )

        st.download_button(
            label="Download customer-entry template",
            data=self.customer_importer.template_bytes(),
            file_name=(
                "health_wellness_customer_entries_template.xlsx"
            ),
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            width="content",
        )

        uploaded = st.file_uploader(
            "Upload customer-entry workbook",
            type=["xlsx"],
            key="customer_entry_import_file",
            width="stretch",
        )

        if (
            uploaded is not None
            and st.button(
                "Import customer entries",
                type="primary",
                key="import_customer_entries",
                width="content",
            )
        ):
            with st.spinner(
                "Importing customer entries..."
            ):
                result = (
                    self.customer_importer
                    .import_workbook(
                        uploaded.getvalue()
                    )
                )

            self._show_result(
                result
            )

    def _render_blood_work_import(
        self,
    ) -> None:
        st.subheader(
            "Blood Work"
        )

        st.write(
            "Import laboratory results using a flexible "
            "test-name/value structure. Example tests "
            "include glucose, A1C, LDL, HDL, hemoglobin, "
            "vitamin D, and many others."
        )

        st.download_button(
            label="Download blood-work template",
            data=self.blood_work_importer.template_bytes(),
            file_name="blood_work_import_template.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            width="content",
        )

        uploaded = st.file_uploader(
            "Upload blood-work workbook",
            type=["xlsx"],
            key="blood_work_import_file",
            width="stretch",
        )

        if (
            uploaded is not None
            and st.button(
                "Import blood work",
                type="primary",
                key="import_blood_work",
                width="content",
            )
        ):
            with st.spinner(
                "Importing blood work..."
            ):
                result = (
                    self.blood_work_importer
                    .import_workbook(
                        uploaded.getvalue()
                    )
                )

            self._show_result(
                result
            )

    @staticmethod
    def _show_result(
        result,
    ) -> None:
        if result.imported > 0:
            st.success(
                f"Imported rows: {result.imported}"
            )

        if result.rejected > 0:
            st.warning(
                f"Rejected rows: {result.rejected}"
            )

            with st.expander(
                "Rejected-row details",
                expanded=True,
            ):
                for error in result.errors[:50]:
                    st.error(
                        error
                    )

        if (
            result.imported == 0
            and result.rejected == 0
        ):
            st.info(
                "No new rows were imported."
            )
