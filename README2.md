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
