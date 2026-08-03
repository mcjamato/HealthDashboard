# Phase 3 Developer Guide

## Files added

- `src/pages/dashboard_page.py`
- `src/pages/analytics_page.py`
- `src/services/correlation_service.py`

## Files replaced

- `src/app.py`
- `src/services/analytics_service.py`
- `src/config.py`
- `requirements.txt`

## CorrelationService

`build_daily_dataset()` converts four record sets into one date-indexed table.

`correlation_matrix()` removes the date column, keeps metrics with at least two
measurements, and calculates Pearson correlations.

`strongest_relationships()` reads only the upper triangle of the matrix so each
pair appears once. Pairs are ordered by absolute coefficient.

## Adding a metric to correlations

1. Add the database and model field in Phase 2 code.
2. Add the field to the correct mapping in `build_daily_dataset()`.
3. Choose `_daily_sum()` for additive daily measurements or `_daily_mean()` for observations.
4. Add a friendly label to `METRIC_LABELS`.
5. Restart Streamlit and enter enough repeated data.

## Percent changes

`percent_change_for_frame()` sorts records chronologically before comparing the
last two valid measurements. This avoids calculating changes from the descending
history order returned by repositories.
