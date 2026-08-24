# Changelog

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

