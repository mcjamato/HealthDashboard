from __future__ import annotations

from collections.abc import Sequence

import pandas as pd
import streamlit as st


class MonthFilter:
    """Reusable month filtering with a compact checkbox popover."""

    @staticmethod
    def prepare(
        frame: pd.DataFrame,
    ) -> pd.DataFrame:
        if frame.empty:
            return frame.copy()

        if "recorded_on" not in frame.columns:
            raise ValueError(
                "MonthFilter requires a 'recorded_on' column."
            )

        prepared = frame.copy()

        prepared["recorded_on"] = pd.to_datetime(
            prepared["recorded_on"],
            errors="coerce",
        )

        return prepared.dropna(
            subset=["recorded_on"]
        )

    @staticmethod
    def available_months(
        frame: pd.DataFrame,
    ) -> list[str]:
        prepared = MonthFilter.prepare(
            frame
        )

        if prepared.empty:
            return []

        periods = (
            prepared["recorded_on"]
            .dt.to_period("M")
            .dropna()
            .unique()
        )

        return [
            period.strftime("%B %Y")
            for period in sorted(
                periods,
                reverse=True,
            )
        ]

    @staticmethod
    def _checkbox_key(
        key_prefix: str,
        month: str,
    ) -> str:
        return (
            f"{key_prefix}_month_"
            f"{month.replace(' ', '_')}"
        )

    @staticmethod
    def select_months(
        frame: pd.DataFrame,
        key_prefix: str,
        label: str = "Months",
    ) -> list[str]:
        """
        Show available months inside a dropdown-style popover.

        The newest available month is selected automatically on first use.
        Users can check additional months to analyze multiple months.
        """

        months = MonthFilter.available_months(
            frame
        )

        if not months:
            st.caption(
                "No dated records are available."
            )
            return []

        newest = months[0]

        # Seed the latest month before the widgets are rendered.
        initialized_key = (
            f"{key_prefix}_months_initialized"
        )

        if not st.session_state.get(
            initialized_key,
            False,
        ):
            for month in months:
                st.session_state[
                    MonthFilter._checkbox_key(
                        key_prefix,
                        month,
                    )
                ] = (
                    month == newest
                )

            st.session_state[
                initialized_key
            ] = True

        currently_selected = [
            month
            for month in months
            if st.session_state.get(
                MonthFilter._checkbox_key(
                    key_prefix,
                    month,
                ),
                False,
            )
        ]

        button_label = (
            currently_selected[0]
            if len(currently_selected) == 1
            else (
                f"{len(currently_selected)} months selected"
                if currently_selected
                else label
            )
        )

        with st.popover(
            button_label,
            width="content",
        ):
            st.markdown(
                f"**{label} to analyze**"
            )

            st.caption(
                "The latest month is selected by default. "
                "Check additional months to extend the analysis."
            )

            selected: list[str] = []

            for month in months:
                key = MonthFilter._checkbox_key(
                    key_prefix,
                    month,
                )

                if st.checkbox(
                    month,
                    key=key,
                ):
                    selected.append(
                        month
                    )

        # Read the state again after the popover renders.
        selected = [
            month
            for month in months
            if st.session_state.get(
                MonthFilter._checkbox_key(
                    key_prefix,
                    month,
                ),
                False,
            )
        ]

        if not selected:
            newest_key = (
                MonthFilter._checkbox_key(
                    key_prefix,
                    newest,
                )
            )

            st.session_state[
                newest_key
            ] = True

            selected = [
                newest
            ]

            st.warning(
                "At least one month must remain selected. "
                f"{newest} has been restored."
            )

        return selected

    @staticmethod
    def filter(
        frame: pd.DataFrame,
        selected_months: Sequence[str],
    ) -> pd.DataFrame:
        prepared = MonthFilter.prepare(
            frame
        )

        if prepared.empty:
            return prepared

        if not selected_months:
            return prepared.iloc[
                0:0
            ].copy()

        labels = (
            prepared["recorded_on"]
            .dt.strftime("%B %Y")
        )

        return prepared[
            labels.isin(
                list(
                    selected_months
                )
            )
        ].copy()

    @staticmethod
    def selection_caption(
        selected_months: Sequence[str],
    ) -> str:
        months = list(
            selected_months
        )

        if not months:
            return "No months selected"

        if len(months) == 1:
            return months[0]

        return ", ".join(
            months
        )
