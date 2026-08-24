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
