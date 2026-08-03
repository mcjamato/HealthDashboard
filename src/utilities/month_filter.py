from __future__ import annotations

import pandas as pd
import streamlit as st


class MonthFilter:
    """Provides a reusable month selector for dashboard data."""

    ALL_MONTHS = "All months"

    @staticmethod
    def apply(
        frame: pd.DataFrame,
        key: str,
        label: str = "Month",
    ) -> tuple[pd.DataFrame, str]:
        """
        Filter a DataFrame by a selected calendar month.

        The DataFrame must contain a recorded_on column.
        """

        if (
            frame.empty
            or "recorded_on" not in frame.columns
        ):
            return (
                frame.copy(),
                MonthFilter.ALL_MONTHS,
            )

        filtered = frame.copy()

        filtered["recorded_on"] = pd.to_datetime(
            filtered["recorded_on"],
            errors="coerce",
        )

        filtered = filtered.dropna(
            subset=["recorded_on"]
        )

        if filtered.empty:
            return (
                filtered,
                MonthFilter.ALL_MONTHS,
            )

        filtered["_month_key"] = (
            filtered["recorded_on"]
            .dt.to_period("M")
        )

        periods = sorted(
            filtered["_month_key"]
            .dropna()
            .unique(),
            reverse=True,
        )

        month_labels = {
            period.strftime("%B %Y"): period
            for period in periods
        }

        options = [
            MonthFilter.ALL_MONTHS,
            *month_labels.keys(),
        ]

        selected = st.selectbox(
            label,
            options,
            key=key,
        )

        if selected != MonthFilter.ALL_MONTHS:
            selected_period = (
                month_labels[selected]
            )

            filtered = filtered[
                filtered["_month_key"]
                == selected_period
            ]

        filtered = filtered.drop(
            columns=["_month_key"]
        )

        return filtered, selected