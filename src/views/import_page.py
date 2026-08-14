import streamlit as st


class ImportPage:
    """Administrator page for downloading and importing Excel workbooks."""

    def __init__(
        self,
        importer,
    ) -> None:
        self.importer = importer

    def render(
        self,
        role: str,
    ) -> None:
        st.title("📥 Excel Import")

        if role != "admin":
            st.warning(
                "Excel importing is available only to administrators."
            )
            return

        st.write(
            "Use the workbook template to import clients and wellness data. "
            "Client email addresses are used to match wellness records to the "
            "correct client profile."
        )

        st.download_button(
            label="Download workbook template",
            data=self.importer.template_bytes(),
            file_name="health_wellness_import_template.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
            use_container_width=True,
        )

        uploaded = st.file_uploader(
            "Upload completed workbook",
            type=["xlsx"],
            help=(
                "The workbook must contain Clients, Exercise, Health, "
                "MentalWellness, and Nutrition worksheets."
            ),
        )

        if uploaded is None:
            return

        if st.button(
            "Import workbook",
            use_container_width=True,
            type="primary",
        ):
            with st.spinner("Importing workbook..."):
                result = self.importer.import_workbook(
                    uploaded.getvalue()
                )

            if result.imported > 0:
                st.success(
                    f"Imported rows: {result.imported}"
                )

            if result.rejected > 0:
                st.warning(
                    f"Rejected rows: {result.rejected}"
                )

                with st.expander(
                    "View rejected-row details",
                    expanded=True,
                ):
                    for error in result.errors[:50]:
                        st.error(error)

            if (
                result.imported == 0
                and result.rejected == 0
            ):
                st.info(
                    "The workbook did not contain any new rows to import."
                )

            if (
                result.imported > 0
                and result.rejected == 0
            ):
                st.success(
                    "Import completed successfully. "
                    "Refreshing the application..."
                )
                st.rerun()
