# Version 1.5.1 - Repository Cleanup

This maintenance release improves repository behavior on macOS and with GitHub Desktop.

## What changed

The `.gitignore` now excludes `.DS_Store` files anywhere in the repository and ignores
Python caches, virtual environments, local editor settings, Streamlit secrets, logs,
and temporary runtime files.

Instead of ignoring every `*.db` file, the project now ignores only the configured
runtime SQLite database:

`health_dashboard.db`

This keeps future demo or sample database files available for intentional Git commits.

## GitHub Desktop

After copying the v1.5.1 files into the repository:

1. Open GitHub Desktop.
2. Select the HealthWellnessDashboard repository.
3. Review the changed files.
4. Confirm `.DS_Store` is no longer shown.
5. Use commit summary:
   `v1.5.1 Clean up macOS and repository ignore rules`
6. Click **Commit to main**.
7. Click **Push origin**.

If an old `.DS_Store` file was previously committed, remove it once with:

`find . -name .DS_Store -delete`

and, if Git still tracks it:

`git rm --cached .DS_Store`
