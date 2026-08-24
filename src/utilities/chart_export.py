from __future__ import annotations

import re

import pandas as pd


class ChartExport:
    """Common CSV and Plotly browser-image export settings."""

    @staticmethod
    def safe_filename(
        value: str,
    ) -> str:
        cleaned = re.sub(
            r"[^A-Za-z0-9_-]+",
            "_",
            value.strip(),
        )
        return cleaned.strip("_") or "chart"

    @staticmethod
    def csv_bytes(
        frame: pd.DataFrame,
    ) -> bytes:
        return frame.to_csv(
            index=False
        ).encode("utf-8")

    @staticmethod
    def plotly_config(
        filename: str,
    ) -> dict:
        """
        Plotly's camera icon downloads a PNG directly in the browser.

        This avoids needing a server-side Chromium/Kaleido installation on
        Streamlit Community Cloud.
        """

        return {
            "displayModeBar": True,
            "displaylogo": False,
            "responsive": True,
            "modeBarButtonsToRemove": [
                "lasso2d",
                "select2d",
            ],
            "toImageButtonOptions": {
                "format": "png",
                "filename": ChartExport.safe_filename(
                    filename
                ),
                "height": 700,
                "width": 1200,
                "scale": 2,
            },
        }
