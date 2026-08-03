import streamlit as st

class ImportPage:
    def __init__(self, importer):
        self.importer = importer

    def render(self, role):
        st.title("📥 Excel Import")
        if role != "admin":
            st.warning("Administrator only.")
            return
        st.download_button(
            "Download workbook template",
            self.importer.template_bytes(),
            "health_wellness_import_template.xlsx",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
        uploaded = st.file_uploader("Upload completed workbook", type=["xlsx"])
        if uploaded and st.button("Import workbook", use_container_width=True):
            result = self.importer.import_workbook(uploaded.getvalue())
            st.success(f"Imported rows: {result.imported}")
            if result.rejected:
                st.warning(f"Rejected rows: {result.rejected}")
            for error in result.errors[:25]:
                st.error(error)
