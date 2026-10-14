# sdt03 · Database Testing in Practice

Practice files for the chapter's screen recording and for Task **HLF-P43 "Bookshop migration sign-off"**.
All data is fictional. Every `.sql` file drops and rebuilds its own schema, so you can run it again at any time.

| File | What it is |
|---|---|
| `demo/harbourleaf_migration.sql` | Harbourleaf practice data used in the video: schema `hl_check` |
| `demo/checks/test_db_checks.py` | The video's database checks as PyTest tests |
| `task/bookshop_migration.sql` | The practice online bookshop (separate from Harbourleaf): schema `bookshop_mig` |
| `task/checks/` | `requirements.txt` and `pytest.ini` for your `test_bookshop.py` |

## Run the checks
From the `checks` folder, in a virtual environment (as in Python for Testers):
```
python -m venv .venv
```
Activate it:
- Windows CMD: `.venv\Scripts\activate`
- macOS, Linux, Codespaces: `source .venv/bin/activate`

Then:
```
pip install -r requirements.txt
pytest -q
```

## Connecting to your database
- **Codespaces** ("SQL & Database Testing (PostgreSQL)" configuration): nothing to set; the connection settings are already there.
- **Your own computer:** set the connection for this terminal session only, and never write a password into a file.
  - Windows CMD: `set LABS_DSN=host=localhost dbname=labs user=postgres` and `set PGPASSWORD=your-password`
  - macOS / Linux: `export LABS_DSN="host=localhost dbname=labs user=postgres"` and `export PGPASSWORD=your-password`

The checks open the connection read-only: they never change the data they check.
