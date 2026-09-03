# Version 1.6.0 - Intake Onboarding and 12-Month Demo Data

## Intake questionnaire

The supplied Wellness Intake Questionnaire is now represented in the database as a one-to-one `client_intake_profiles` record linked to each client. The implementation preserves all 13 questionnaire sections, including identity/context, goals, medical and health history, body metrics, nutrition, activity, sleep, mental wellness, lifestyle, readiness, program preferences, notes, and consent.

## Manual onboarding

Administrators can use **Client Profiles** to create a client and complete the same questionnaire fields/options used by the import template. Name and email remain the required identity fields; the rest of the questionnaire can be completed as available.

## Excel and CSV imports

The **Customer + Intake** import destination supports:
- `.xlsx`: Clients/intake plus Exercise, Health, MentalWellness, and Nutrition worksheets.
- `.csv`: client identity and intake questionnaire only.

Multi-select questionnaire answers are stored using semicolon-separated values in spreadsheet imports.

## Administrator intake view

The administrator's main Dashboard includes **View full client intake information**. The expander shows the selected client's identity plus every saved questionnaire section. Client logins do not receive this administrator-only view.

## Month-default fix

The latest available month is established before the checkbox widgets are created. Month state is also scoped to the selected client. This removes the first-login state problem where the dashboard could error until a month was manually chosen.

## Demo dataset

The new sample workbook contains 10 fictional clients and daily data from **September 1, 2025 through August 31, 2026**.

Record counts after a clean smoke-test import:
- Clients: 10
- Intake profiles: 10
- Exercise: 3,650
- Health: 3,650
- Mental Wellness: 3,650
- Nutrition: 3,650
- Total imported rows: 14,610
- Rejected rows: 0

Because August 2026 is the newest month in the sample data, August is the automatic dashboard month after import/login.
