# Version 1.6.1 - Streamlit Cloud Importer Fix

## Problem

Streamlit Community Cloud reported:

`TypeError: ExcelImporter.__init__() takes 6 positional arguments but 7 were given`

This indicates `src/app.py` and `src/imports/excel_importer.py` came from different release states. The new intake repository was being supplied by the app while the deployed importer still used the older constructor.

## Fix

- `ExcelImporter` keeps the legacy positional repository order.
- The new intake repository is an optional final argument.
- `app.py` passes all dependencies by keyword.
- The full v1.6.1 release should be deployed to eliminate mixed-version files.

## Streamlit Cloud

Push v1.6.1 to GitHub and then reboot/redeploy the Streamlit app. No database schema change is required for this patch.
