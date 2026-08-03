# Phase 3 Design Document

## Scope

Phase 3 converts the four isolated wellness modules into an analytics platform.

## New components

- `DashboardPage`: client summary metrics, percent changes, and trend charts.
- `AnalyticsPage`: combined daily dataset, correlation matrix, insights, and scatter exploration.
- `CorrelationService`: normalizes dates, aggregates same-day entries, joins domains, and calculates Pearson correlations.
- Expanded `AnalyticsService`: chronological percent changes, totals, latest values, and formatting.

## Cross-domain data flow

1. Repositories load all active records for the selected client.
2. Exercise and nutrition entries are summed by day because multiple activities or meals may occur.
3. Health and mental-wellness entries are averaged by day if multiple observations occur.
4. Daily tables are outer-joined on `recorded_on`.
5. Numeric columns with at least two observations enter the Pearson correlation matrix.
6. Unique metric pairs are ranked by absolute correlation strength.

## Aggregation rules

- Exercise: daily sum of minutes, calories burned, and steps.
- Health: daily mean of sleep, weight, sleep quality, and water.
- Mental wellness: daily mean of mood, stress, energy, focus, and meditation.
- Nutrition: daily sum of calories, macronutrients, fiber, and water.

## Interpretation

A coefficient near `1` indicates two metrics tend to increase together.
A coefficient near `-1` indicates one tends to increase while the other decreases.
A value near `0` indicates little linear association.

Correlation is exploratory and does not establish causation.

## Permissions

Both administrators and clients can view their available analytics.
Only administrators retain historical deactivation controls on domain pages.
