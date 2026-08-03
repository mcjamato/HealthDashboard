# Phase 3 Deployment Guide

## Upgrade from Phase 2

Copy the Phase 3 changed files into the matching Phase 2 paths. Do not delete
`src/database/health_dashboard.db` when you want to retain entered records.

Install the new dependency:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Run:

```bash
streamlit run src/app.py
```

## Test sequence

1. Select an existing client.
2. Enter records on at least three dates in every domain.
3. Open Dashboard and verify metric cards and trend charts.
4. Open Cross-Domain Analytics.
5. Verify the combined daily table.
6. Verify the matrix and strongest-relationship list.
7. Select two metrics and inspect the scatter chart.

## GitHub Desktop

Use this commit message:

`Phase 3 - Add dashboard and cross-domain analytics`

Then choose **Push origin**.
