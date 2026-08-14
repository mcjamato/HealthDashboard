from io import BytesIO

import pandas as pd


class ExcelExportService:
    @staticmethod
    def client_workbook(
        client,
        exercise,
        health,
        mental,
        nutrition,
        correlations,
    ) -> bytes:
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            pd.DataFrame([client]).to_excel(
                writer, sheet_name="Client", index=False
            )
            exercise.to_excel(writer, sheet_name="Exercise", index=False)
            health.to_excel(writer, sheet_name="Health", index=False)
            mental.to_excel(writer, sheet_name="MentalWellness", index=False)
            nutrition.to_excel(writer, sheet_name="Nutrition", index=False)
            correlations.to_excel(writer, sheet_name="Correlations")
        return output.getvalue()
