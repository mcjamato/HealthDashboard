# Changelog

All notable changes to the Health & Wellness Analytics Dashboard will be recorded here.

## [1.2.1] - Client Import Workflow

### Added
- Formal project changelog.
- Demonstration workbook containing 20 clients and six months of wellness data.
- Automatic application refresh after a successful Excel import.

### Improved
- Excel imports identify clients by email instead of hard-coded SQLite client IDs.
- Existing clients are matched by email and are not duplicated during repeat imports.
- Exercise, Health, Mental Wellness, and Nutrition rows resolve the correct database client ID automatically.
- Import errors are reported row by row without preventing valid rows from loading.

### Import Workbook
The supported workbook contains five worksheets:

- Clients
- Exercise
- Health
- MentalWellness
- Nutrition

The four wellness worksheets use `client_email` as the external client identifier.

## [1.2.0] - Consolidated Application

### Added
- Complete consolidated application baseline.
- Administrator and client authentication.
- bcrypt password hashing.
- Client-specific role restrictions.
- Grouped navigation.
- Main analytics dashboard.
- Customer domain dashboards.
- Monthly chart filters.
- KPI cards and interactive Plotly charts.
- Cross-domain Pearson correlation analysis.
- Excel workbook import.
- PDF client reports.
- Excel administrator reports.
- Report schedule configuration.
- Final acceptance-test page.
- Twenty-client six-month demonstration dataset.

## [1.1.0] - Dashboard UI Polish

### Added
- Client summary header.
- Improved dashboard KPI presentation.
- Reusable dashboard layout components.
- Compact month filter.
- Responsive dashboard layout.

## [1.0.0] - MVP

### Added
- Client onboarding.
- Exercise tracking.
- Health tracking.
- Mental Wellness tracking.
- Nutrition tracking.
- SQLite persistence.
- Administrator/client role model.
- Basic analytics and reporting.
