# Health & Wellness Analytics Dashboard

A compact Streamlit + SQLite analytics platform with:

- Administrator and client logins
- Client onboarding
- Exercise, Health, Mental Wellness, and Nutrition data entry
- Monthly dashboard filtering
- Client-specific dashboards
- Trend charts and correlation analytics
- Excel workbook import
- PDF client reports and Excel administrator reports
- Report schedule configuration
- Sample data for demonstrations

## First run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py
```

The first launch creates an administrator account if none exists.

Default development credentials:

```text
username: admin
password: ChangeMe123!
```

For deployment, set environment variables instead:

```bash
export WELLNESS_ADMIN_USERNAME="admin"
export WELLNESS_ADMIN_PASSWORD="your-strong-password"
streamlit run src/app.py
```

## Sample data

Use:

`sample_data/HealthWellness_Demo_20Clients_6Months.xlsx`

The importer resolves client records by email address, so the workbook can be
used with a fresh or already-populated database.


## Version 1.3.0 features

- CSV export under dashboard graphs
- PNG graph export from each Plotly chart's camera icon
- Customer Entries / Blood Work Data Import selector
- Blood-work tracking
- Administrator and client password changes
- Optional nutrition food-photo analysis

### Streamlit Community Cloud - Food Photo Analyzer

In Streamlit Cloud, open your app's **Settings -> Secrets** and add:

```toml
OPENAI_API_KEY = "your-api-key"
OPENAI_VISION_MODEL = "gpt-5.6-luna"
```

Do not commit real API keys to GitHub.

The application still runs without an OpenAI key; only the Food Photo Analyzer
is disabled.


## Client login experience

Client logins are created by an administrator under:

`Customer Data -> User Accounts`

Each client login is linked to one client profile. After login, the client sees
only Customer Dashboards and the wellness data-entry pages required for their
own account. Clients cannot select or view another customer.


## Version 1.4.0 dashboard filtering

Dashboard views open with the newest available month checked automatically.
Users can check additional Month Year values to compare multiple months. Only
the newest month is shown initially.


## Version 1.5.0

- Dashboard month selection uses a compact popover with one checkbox per month.
- Latest available month is selected by default.
- Administrators can expand the selected client's full stored intake profile.
- Cross-Domain Analytics provides selectable metric-pair scatter plots.
- Correlation analysis exports CSV and Excel data.


## Version 1.5.1

Repository cleanup for macOS, GitHub Desktop, and Streamlit Cloud.

- `.DS_Store` files are ignored.
- Streamlit secrets remain outside Git.
- Python cache and virtual-environment files are ignored.
- The application ignores only its runtime SQLite database: `health_dashboard.db`.
- Demo/sample assets remain trackable in GitHub.


## Version 1.6.0

Version 1.6.0 adds the full 13-section Wellness Intake Questionnaire to client onboarding. Administrators can create clients manually using the questionnaire or import client/intake data from Excel or CSV. The main administrator dashboard can expand the selected client's complete intake profile.

The included demo workbook contains 10 fictional clients and daily data from September 2025 through August 2026. The dashboard automatically uses the newest available month on first render, so August 2026 opens without requiring the user to select a month first.

Sample files are in `sample_data/`:
- `HealthWellness_Demo_10Clients_12Months_v1.6.0.xlsx`
- `Wellness_Intake_Import_Template_v1.6.0.xlsx`
- `Wellness_Intake_Import_Template_v1.6.0.csv`
- `Wellness_Intake_10Clients_v1.6.0.csv`
