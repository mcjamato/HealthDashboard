from __future__ import annotations

from collections.abc import Sequence

import pandas as pd
import streamlit as st


class MonthFilter:
    """Reusable month filtering with a latest-month default."""

    @staticmethod
    def prepare(frame: pd.DataFrame) -> pd.DataFrame:
        if frame.empty:
            return frame.copy()
        if "recorded_on" not in frame.columns:
            raise ValueError("MonthFilter requires a 'recorded_on' column.")
        prepared = frame.copy()
        prepared["recorded_on"] = pd.to_datetime(prepared["recorded_on"], errors="coerce")
        return prepared.dropna(subset=["recorded_on"])

    @staticmethod
    def available_months(frame: pd.DataFrame) -> list[str]:
        prepared = MonthFilter.prepare(frame)
        if prepared.empty:
            return []
        periods = prepared["recorded_on"].dt.to_period("M").dropna().unique()
        return [period.strftime("%B %Y") for period in sorted(periods, reverse=True)]

    @staticmethod
    def _checkbox_key(key_prefix: str, month: str) -> str:
        return f"{key_prefix}_month_{month.replace(' ', '_')}"

    @staticmethod
    def select_months(frame: pd.DataFrame, key_prefix: str, label: str = "Months") -> list[str]:
        months = MonthFilter.available_months(frame)
        if not months:
            st.caption("No dated records are available.")
            return []

        newest = months[0]
        initialized_key = f"{key_prefix}_months_initialized"

        # Initialize state BEFORE any checkbox widget exists. This prevents the
        # Streamlit session-state error that could occur on the first login/render.
        if initialized_key not in st.session_state:
            st.session_state[initialized_key] = True
            for month in months:
                st.session_state[MonthFilter._checkbox_key(key_prefix, month)] = (month == newest)
        else:
            # New months may appear after an import. Seed missing checkbox keys safely.
            for month in months:
                key = MonthFilter._checkbox_key(key_prefix, month)
                if key not in st.session_state:
                    st.session_state[key] = False

        current = [
            month for month in months
            if bool(st.session_state.get(MonthFilter._checkbox_key(key_prefix, month), False))
        ]
        if not current:
            # Do not mutate a widget-backed state key after rendering. Use newest
            # as the effective range for this render; next interaction can check it.
            current = [newest]

        button_label = current[0] if len(current) == 1 else f"{len(current)} months selected"
        selected = []
        with st.popover(button_label, width="content"):
            st.markdown(f"**{label} to analyze**")
            st.caption("The newest available month is selected automatically. Check more months to compare longer trends.")
            for month in months:
                key = MonthFilter._checkbox_key(key_prefix, month)
                if st.checkbox(month, key=key):
                    selected.append(month)

        return selected or [newest]

    @staticmethod
    def filter(frame: pd.DataFrame, selected_months: Sequence[str]) -> pd.DataFrame:
        prepared = MonthFilter.prepare(frame)
        if prepared.empty:
            return prepared
        if not selected_months:
            selected_months = MonthFilter.available_months(prepared)[:1]
        labels = prepared["recorded_on"].dt.strftime("%B %Y")
        return prepared[labels.isin(list(selected_months))].copy()

    @staticmethod
    def selection_caption(selected_months: Sequence[str]) -> str:
        months = list(selected_months)
        if not months:
            return "Latest month"
        return months[0] if len(months) == 1 else ", ".join(months)
