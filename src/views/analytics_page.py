import pandas as pd
import plotly.express as px
import streamlit as st

from components.layout import DashboardLayout
from services.correlation_service import CorrelationService
from utilities.data_export import DataExport
from utilities.month_filter import MonthFilter


class AnalyticsPage:
    """Interactive cross-domain correlation analysis."""

    def __init__(
        self,
        exercise,
        health,
        mental,
        nutrition,
    ) -> None:
        self.exercise = exercise
        self.health = health
        self.mental = mental
        self.nutrition = nutrition
        self.correlations = (
            CorrelationService()
        )

    def render(
        self,
        client_id: int | None,
    ) -> None:
        st.title(
            "🔗 Cross-Domain Analytics"
        )

        st.caption(
            "Choose two metrics to analyze their relationship. "
            "Correlation describes association and does not prove causation."
        )

        if client_id is None:
            st.info(
                "Select a client to run correlations."
            )
            return

        daily = (
            self.correlations
            .build_daily_dataset(
                self.exercise.list_for_client(
                    client_id
                ),
                self.health.list_for_client(
                    client_id
                ),
                self.mental.list_for_client(
                    client_id
                ),
                self.nutrition.list_for_client(
                    client_id
                ),
            )
        )

        if len(
            daily
        ) < 2:
            st.warning(
                "At least two matching dates are required."
            )
            return

        selected_months = (
            DashboardLayout
            .render_filter_bar(
                render_filter=lambda: (
                    MonthFilter.select_months(
                        daily,
                        key_prefix=(
                            f"correlation_analysis_{client_id}"
                        ),
                        label="Months",
                    )
                ),
                title="Analysis range",
                width_ratio=(
                    1,
                    4,
                ),
            )
        )

        filtered_daily = (
            MonthFilter.filter(
                daily,
                selected_months,
            )
        )

        if len(
            filtered_daily
        ) < 2:
            st.warning(
                "The selected month range does not contain "
                "enough overlapping data."
            )
            return

        metrics = (
            self.correlations
            .available_metrics(
                filtered_daily
            )
        )

        if len(
            metrics
        ) < 2:
            st.warning(
                "At least two numeric metrics with repeated "
                "measurements are required."
            )
            return

        metric_labels = (
            self.correlations
            .METRIC_LABELS
        )

        label_to_metric = {
            metric_labels.get(
                metric,
                metric.replace(
                    "_",
                    " ",
                ).title(),
            ): metric
            for metric in metrics
        }

        labels = list(
            label_to_metric.keys()
        )

        default_x_label = next(
            (
                label
                for label, metric
                in label_to_metric.items()
                if metric
                == "exercise_minutes"
            ),
            labels[
                0
            ],
        )

        default_y_label = next(
            (
                label
                for label, metric
                in label_to_metric.items()
                if metric
                == "mood_score"
            ),
            labels[
                1
                if len(
                    labels
                ) > 1
                else 0
            ],
        )

        filter_one, filter_two = st.columns(
            2
        )

        with filter_one:
            x_label = st.selectbox(
                "X metric",
                labels,
                index=labels.index(
                    default_x_label
                ),
                key="correlation_x_metric",
            )

        with filter_two:
            y_options = [
                label
                for label in labels
                if label != x_label
            ]

            if (
                default_y_label
                not in y_options
            ):
                default_y_label = y_options[
                    0
                ]

            y_label = st.selectbox(
                "Y metric",
                y_options,
                index=y_options.index(
                    default_y_label
                ),
                key="correlation_y_metric",
            )

        x_metric = label_to_metric[
            x_label
        ]

        y_metric = label_to_metric[
            y_label
        ]

        pair_data = (
            self.correlations
            .pair_data(
                filtered_daily,
                x_metric,
                y_metric,
            )
        )

        result = (
            self.correlations
            .correlate(
                filtered_daily,
                x_metric,
                y_metric,
            )
        )

        if (
            result is None
            or len(
                pair_data
            ) < 2
        ):
            st.warning(
                "These two metrics do not have enough "
                "overlapping observations in the selected months."
            )
            return

        metric_columns = st.columns(
            3
        )

        metric_columns[
            0
        ].metric(
            "Pearson r",
            f"{result.coefficient:.3f}",
        )

        metric_columns[
            1
        ].metric(
            "Relationship",
            (
                f"{result.strength} "
                f"{result.direction.lower()}"
            ),
        )

        metric_columns[
            2
        ].metric(
            "Matched days",
            len(
                pair_data
            ),
        )

        scatter = px.scatter(
            pair_data,
            x=x_metric,
            y=y_metric,
            trendline="ols",
            labels={
                x_metric: x_label,
                y_metric: y_label,
            },
            hover_data={
                "recorded_on": True,
                x_metric: ":.2f",
                y_metric: ":.2f",
            },
            title=(
                f"{y_label} vs {x_label}"
            ),
        )

        scatter.update_traces(
            marker={
                "size": 9,
            }
        )

        DashboardLayout.render_exportable_chart(
            title=(
                f"{y_label} vs {x_label}"
            ),
            figure=scatter,
            data=pair_data,
            filename=(
                f"correlation_"
                f"{x_metric}_"
                f"{y_metric}"
            ),
            key="selected_correlation",
        )

        export_one, export_two = st.columns(
            2
        )

        with export_one:
            st.download_button(
                "Download selected correlation CSV",
                data=DataExport.csv_bytes(
                    pair_data
                ),
                file_name=(
                    f"{x_metric}_vs_{y_metric}.csv"
                ),
                mime="text/csv",
                width="stretch",
            )

        matrix = (
            self.correlations
            .correlation_matrix(
                filtered_daily
            )
        )

        matrix_export = (
            matrix.reset_index()
            .rename(
                columns={
                    "index": "metric"
                }
            )
            if not matrix.empty
            else pd.DataFrame()
        )

        with export_two:
            st.download_button(
                "Download analysis Excel",
                data=DataExport.excel_bytes(
                    {
                        "Selected Pair": pair_data,
                        "Daily Data": filtered_daily,
                        "Correlation Matrix": matrix_export,
                    }
                ),
                file_name="correlation_analysis.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
                width="stretch",
            )

        with st.expander(
            "View full correlation matrix",
            expanded=False,
        ):
            if matrix.empty:
                st.info(
                    "The full matrix is not available "
                    "for this month selection."
                )
            else:
                display_matrix = matrix.copy()

                display_matrix.index = [
                    metric_labels.get(
                        metric,
                        metric,
                    )
                    for metric in display_matrix.index
                ]

                display_matrix.columns = [
                    metric_labels.get(
                        metric,
                        metric,
                    )
                    for metric in display_matrix.columns
                ]

                st.dataframe(
                    display_matrix.round(
                        3
                    ),
                    width="stretch",
                )

        with st.expander(
            "View combined daily data",
            expanded=False,
        ):
            st.dataframe(
                filtered_daily,
                width="stretch",
                hide_index=True,
            )

            st.download_button(
                "Download combined daily CSV",
                data=DataExport.csv_bytes(
                    filtered_daily
                ),
                file_name=(
                    "cross_domain_daily_data.csv"
                ),
                mime="text/csv",
                width="content",
            )
