# Health & Wellness Analytics Dashboard - Design Overview

## Purpose

This project is a small health and wellness analytics platform built for teaching
software development, data management, and dashboard analytics. One administrator
manages many clients. Clients can log in, enter new wellness data, and view their
own history and analytics.

## Technology

- Python for application logic
- Streamlit for the web interface
- SQLite3 for local relational storage
- Pandas for data preparation
- Plotly for interactive charts and hover details
- ReportLab for PDF reports
- OpenPyXL for Excel import/export
- bcrypt for password hashing

Streamlit was selected because the application is intentionally compact and
analytics-focused. It provides fast development, interactive widgets, and direct
integration with Pandas and Plotly.

## Architecture

The application uses a layered structure:

- `views/` contains screens and forms.
- `components/` contains reusable dashboard layout helpers.
- `models/` contains typed domain records.
- `repositories/` owns SQLite queries.
- `services/` performs calculations and correlation analysis.
- `imports/` validates and loads Excel workbooks.
- `reports/` creates PDF and Excel exports.
- `auth/` handles authentication and session state.
- `utilities/` contains reusable filters and client display helpers.

## Data Model

The central `clients` table is related one-to-many to:

- `exercise_records`
- `health_records`
- `mental_wellness_records`
- `nutrition_records`

The `users` table stores administrator or client login accounts. Client accounts
are linked to exactly one client profile. `scheduled_reports` stores report
schedule configuration.

## Analytics

Each domain supports historical viewing and trend charts. The main dashboard
shows monthly-filtered KPI cards and interactive Plotly charts. Cross-domain
analytics aggregate records to one row per date and calculate Pearson
correlations between numeric wellness metrics.

## Import and Reporting

The official Excel workbook contains Clients, Exercise, Health, MentalWellness,
and Nutrition worksheets. Domain sheets identify clients by email, which is
resolved to the correct SQLite client ID during import.

Clients can download PDF wellness reports. Administrators can also download
Excel workbooks and configure recurring report schedules.

## Security and Permissions

Passwords are stored as bcrypt hashes. Administrators can manage clients,
accounts, imports, schedules, and all client data. Client users are restricted
to their linked client profile and cannot switch to another client's data.

## Current Scope

The application is an educational MVP. Goals and notifications are intentionally
deferred, and stored report schedules require an external scheduler such as
launchd, cron, GitHub Actions, or a hosted job runner for unattended execution.
