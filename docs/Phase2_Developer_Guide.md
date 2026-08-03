# Phase 2 Developer Guide

## Entry point

`src/app.py` initializes Streamlit, injects CSS, initializes SQLite, constructs repositories, and routes to page classes.

## Important classes

- `DatabaseManager`: connection lifecycle and schema setup.
- `ExerciseRecord`, `HealthRecord`, `MentalWellnessRecord`, `NutritionRecord`: typed data carriers.
- `DomainRepository`: reusable create/list/deactivate behavior.
- Four concrete repositories: table and column mappings.
- `AnalyticsService`: latest value, average, percent change, chronological preparation.
- Page classes: form handling, validation, summaries, charts, and history.

## Adding a field

1. Add the column in `schema.sql` or a migration.
2. Add the dataclass field.
3. Add the repository column mapping.
4. Add a Streamlit control.
5. Add optional summary/chart logic.
6. Add a test.

## Permissions

The demo role selector keeps this phase independently runnable. When Phase 1 authentication is connected, replace the demo role and client selection with authenticated session values.
