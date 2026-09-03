# Changelog

## [1.5.1] - macOS and Git Repository Cleanup

### Changed
- Added macOS `.DS_Store` exclusions for GitHub Desktop.
- Added common Python cache and virtual-environment exclusions.
- Added Streamlit secrets exclusion.
- Added local editor/cache exclusions.
- Removed the broad `*.db` approach.
- The runtime SQLite database is now ignored specifically as `health_dashboard.db`.
- SQLite journal/WAL/SHM sidecar files for that runtime database are ignored.
- `sample_data/` and `docs/` are explicitly retained in Git.
- Application version updated to 1.5.1.

### Notes
- The demo Excel workbook remains trackable in GitHub.
- A future demo/sample SQLite database can also be committed intentionally because all `.db` files are no longer globally ignored.

## [1.5.0] - Dashboard Range, Intake Details, and Correlation Analysis

### Added
- Dropdown-style month selector using a Streamlit popover with a checkbox next to every available month.
- Latest available month remains the default graph range.
- Administrator-only expandable client intake information on the main Dashboard.
- Selectable X and Y metrics on Cross-Domain Analytics.
- Scatter-plot correlation graph with least-squares trend line.
- Pearson correlation coefficient, relationship strength, direction, and matched-day count.
- CSV export for the selected correlation pair.
- Excel export containing the selected pair, combined daily data, and full correlation matrix.
- Expandable full correlation matrix table and combined daily data table.

### Changed
- Correlation analysis no longer depends on a matrix heat-map chart.
- Month filters remain compact until the user opens the month-selection popover.
- Application version updated to 1.5.0.

### Administration
- Full intake information is visible only on the administrator's main Dashboard.
- Client users continue to see their normal dashboard and data-entry experience without the intake-information expander.

## [1.4.0] - Multi-Month Dashboard Filters

### Added
- Checkbox-based month selection on the main dashboard.
- Checkbox-based month selection on all customer dashboards.
- Support for selecting multiple months simultaneously.
- Selection summary showing the active Month Year values.

### Changed
- The newest available month is selected by default when a dashboard opens.
- Only the latest month is displayed initially.
- The previous All Months selector has been removed from dashboard views.
- At least one month must remain selected.
- Application version updated to 1.4.0.

## [1.3.1] - Client Role Navigation

### Added
- Dedicated role-based navigation configuration.
- Client-only menu containing Customer Dashboards and Customer Data entry pages.
- Secondary authorization check before page routing.

### Changed
- Client accounts no longer see the Analyze section.
- Client accounts no longer see Client Profiles, User Accounts, Data Import, or Final Testing.
- Client accounts remain permanently linked to their own client ID and cannot select another customer.
- Client navigation includes Exercise, Health, Mental Wellness, Nutrition, Blood Work, and Change Password.
- Administrator navigation remains unchanged.
- Application version updated to 1.3.1.

### Security
- Page visibility and page authorization are both enforced from the authenticated role.
- A client account must have a valid linked client_id before its data can be displayed.

## [1.3.0] - Export, Blood Work, Food Vision, and Password Management

### Added
- CSV download for dashboard and analytics charts.
- PNG graph download through the Plotly camera icon on every exportable chart.
- Data Import destination selector with Customer Entries and Blood Work options.
- Flexible blood-work database table, importer, manual entry, history, and trend chart.
- Nutrition Food Photo Analyzer using camera or image upload when an OpenAI API secret is configured.
- Self-service password change for administrators and clients.
- Administrator password-reset controls for active accounts.
- Streamlit Cloud secrets example for the optional food-photo analyzer.

### Changed
- Excel Import navigation is now named Data Import.
- Chart rendering is centralized in reusable exportable-chart components.
- Application version updated to 1.3.0.

### Notes
- Food-photo nutrition values are estimates and are labeled accordingly.
- The Plotly camera icon performs PNG export in the user's browser, avoiding a server-side browser dependency on Streamlit Community Cloud.

## [1.2.2] - Streamlit Compatibility Cleanup

### Changed
- Replaced deprecated `use_container_width=True` with `width="stretch"` throughout the application.
- Replaced deprecated `use_container_width=False` with `width="content"` where applicable.
- Updated the displayed application version to 1.2.2.

### Validation
- All Python files passed syntax compilation.
- No remaining `use_container_width` references remain in `src/`.

