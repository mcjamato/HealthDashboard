from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO

import pandas as pd


@dataclass
class BloodWorkImportResult:
    imported: int
    rejected: int
    errors: list[str]


class BloodWorkImporter:
    """Imports flexible laboratory results from an Excel workbook."""

    SHEET_NAME = "BloodWork"

    COLUMNS = [
        "client_email",
        "recorded_on",
        "test_name",
        "value",
        "unit",
        "reference_low",
        "reference_high",
        "notes",
    ]

    def __init__(
        self,
        clients,
        blood_work_repository,
    ) -> None:
        self.clients = clients
        self.repository = blood_work_repository

    @staticmethod
    def template_bytes(
    ) -> bytes:
        output = BytesIO()

        template = pd.DataFrame(
            columns=BloodWorkImporter.COLUMNS
        )

        with pd.ExcelWriter(
            output,
            engine="openpyxl",
        ) as writer:
            template.to_excel(
                writer,
                sheet_name=BloodWorkImporter.SHEET_NAME,
                index=False,
            )

        return output.getvalue()

    def import_workbook(
        self,
        content: bytes,
    ) -> BloodWorkImportResult:
        try:
            workbook = pd.ExcelFile(
                BytesIO(content)
            )
        except Exception as exc:
            return BloodWorkImportResult(
                0,
                1,
                [f"Workbook could not be opened: {exc}"],
            )

        if self.SHEET_NAME not in workbook.sheet_names:
            return BloodWorkImportResult(
                0,
                1,
                [
                    "Blood-work workbook must contain "
                    "a BloodWork worksheet."
                ],
            )

        frame = pd.read_excel(
            workbook,
            sheet_name=self.SHEET_NAME,
        )

        missing = [
            column
            for column in self.COLUMNS
            if column not in frame.columns
        ]

        if missing:
            return BloodWorkImportResult(
                0,
                len(frame),
                [f"Missing columns: {missing}"],
            )

        imported = 0
        rejected = 0
        errors: list[str] = []

        for index, row in frame.iterrows():
            try:
                email = row.get(
                    "client_email"
                )

                if pd.isna(email):
                    raise ValueError(
                        "client_email is required"
                    )

                client = self.clients.get_by_email(
                    str(email)
                )

                if client is None:
                    raise ValueError(
                        f"Unknown client_email: {email}"
                    )

                recorded_on = row.get(
                    "recorded_on"
                )

                if pd.isna(recorded_on):
                    raise ValueError(
                        "recorded_on is required"
                    )

                test_name = row.get(
                    "test_name"
                )

                if (
                    pd.isna(test_name)
                    or not str(test_name).strip()
                ):
                    raise ValueError(
                        "test_name is required"
                    )

                value = row.get(
                    "value"
                )

                if pd.isna(value):
                    raise ValueError(
                        "value is required"
                    )

                def optional_number(
                    item,
                ):
                    return (
                        None
                        if pd.isna(item)
                        else float(item)
                    )

                def optional_text(
                    item,
                ):
                    return (
                        ""
                        if pd.isna(item)
                        else str(item)
                    )

                self.repository.create(
                    {
                        "client_id": int(
                            client["id"]
                        ),
                        "recorded_on": pd.to_datetime(
                            recorded_on
                        ).date().isoformat(),
                        "test_name": str(
                            test_name
                        ).strip(),
                        "value": float(
                            value
                        ),
                        "unit": optional_text(
                            row.get("unit")
                        ),
                        "reference_low": optional_number(
                            row.get("reference_low")
                        ),
                        "reference_high": optional_number(
                            row.get("reference_high")
                        ),
                        "notes": optional_text(
                            row.get("notes")
                        ),
                    }
                )

                imported += 1

            except Exception as exc:
                rejected += 1
                errors.append(
                    f"BloodWork row "
                    f"{index + 2}: {exc}"
                )

        return BloodWorkImportResult(
            imported,
            rejected,
            errors,
        )
