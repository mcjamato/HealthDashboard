# Phase 4 Deployment Guide

## Run

```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/app.py
```

## Git checkpoint

```bash
git add .
git commit -m "Phase 4 - Complete imports reports scheduling and final testing"
git push
git tag -a v1.0.0 -m "Health Wellness Dashboard MVP"
git push origin v1.0.0
```
