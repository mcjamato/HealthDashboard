# Phase 2 Deployment Guide

## macOS setup

```bash
cd HealthWellnessDashboard_Phase2
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run src/app.py
```

## Reset demo data

Stop Streamlit, delete `src/database/health_dashboard.db`, and restart the application.

## GitHub Desktop workflow

1. Add the Phase 2 folder as the local repository, or copy the Phase 2 files into the existing repository.
2. Review the changed files.
3. Enter `Phase 2 - Add four wellness modules` as the commit summary.
4. Commit to the selected branch.
5. Select Push origin.

## Troubleshooting

- `ModuleNotFoundError`: activate `.venv` and reinstall requirements.
- Port already used: `streamlit run src/app.py --server.port 8502`.
- Schema mismatch after development changes: delete the local demo database and restart.
