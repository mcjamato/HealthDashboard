from __future__ import annotations

from datetime import date

import streamlit as st

from configuration.intake_fields import INTAKE_SECTIONS


class IntakeForm:
    """Renders questionnaire fields shared by manual onboarding and edits."""

    @staticmethod
    def _existing(existing: dict | None, key: str, default=None):
        if not existing:
            return default
        value = existing.get(key, default)
        return default if value is None else value

    @staticmethod
    def _multi_value(value) -> list[str]:
        if value is None or value == "":
            return []
        if isinstance(value, list):
            return value
        return [item.strip() for item in str(value).split(";") if item.strip()]

    @classmethod
    def render_fields(cls, existing: dict | None = None, key_prefix: str = "intake") -> dict:
        values = {}
        for section, fields in INTAKE_SECTIONS:
            with st.expander(section, expanded=(section.startswith("1."))):
                for field in fields:
                    key = field["key"]
                    label = field["label"]
                    widget_key = f"{key_prefix}_{key}"
                    field_type = field["type"]
                    current = cls._existing(existing, key)

                    if field_type == "text":
                        values[key] = st.text_input(label, value=str(current or ""), key=widget_key)
                    elif field_type == "textarea":
                        values[key] = st.text_area(label, value=str(current or ""), key=widget_key)
                    elif field_type == "select":
                        options = field["options"]
                        index = options.index(current) if current in options else 0
                        values[key] = st.selectbox(label, options, index=index, key=widget_key)
                    elif field_type == "multiselect":
                        valid = [v for v in cls._multi_value(current) if v in field["options"]]
                        values[key] = st.multiselect(label, field["options"], default=valid, key=widget_key)
                    elif field_type in {"number", "number_optional"}:
                        min_v=float(field.get("min", 0.0)); max_v=float(field.get("max", 10000.0)); step=float(field.get("step", 0.1))
                        if field_type == "number_optional":
                            enabled = st.checkbox(f"Provide {label}", value=current not in (None, ""), key=f"{widget_key}_enabled")
                            values[key] = st.number_input(label, min_value=min_v, max_value=max_v, value=float(current or min_v), step=step, key=widget_key) if enabled else None
                        else:
                            values[key] = st.number_input(label, min_value=min_v, max_value=max_v, value=float(current or min_v), step=step, key=widget_key)
                    elif field_type == "integer_optional":
                        enabled = st.checkbox(f"Provide {label}", value=current not in (None, ""), key=f"{widget_key}_enabled")
                        values[key] = st.number_input(label, min_value=int(field.get("min", 0)), max_value=int(field.get("max", 100)), value=int(current or field.get("min", 0)), step=1, key=widget_key) if enabled else None
                    elif field_type == "checkbox":
                        values[key] = st.checkbox(label, value=bool(current), key=widget_key)
                    elif field_type == "date_optional":
                        enabled = st.checkbox(f"Provide {label}", value=current not in (None, ""), key=f"{widget_key}_enabled")
                        if enabled:
                            try:
                                default_date = date.fromisoformat(str(current)) if current else date.today()
                            except ValueError:
                                default_date = date.today()
                            values[key] = st.date_input(label, value=default_date, key=widget_key).isoformat()
                        else:
                            values[key] = None
        return values
