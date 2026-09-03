from __future__ import annotations

from io import BytesIO

import pandas as pd


class DataExport:
    """Reusable CSV and Excel byte generation."""

    @staticmethod
    def csv_bytes(
        frame: pd.DataFrame,
    ) -> bytes:
        return frame.to_csv(
            index=False
        ).encode(
            "utf-8"
        )

    @staticmethod
    def excel_bytes(
        sheets: dict[str, pd.DataFrame],
    ) -> bytes:
        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl",
        ) as writer:
            for sheet_name, frame in sheets.items():
                safe_name = (
                    sheet_name[
                        :31
                    ]
                )

                frame.to_excel(
                    writer,
                    sheet_name=safe_name,
                    index=False,
                )

        return output.getvalue()
