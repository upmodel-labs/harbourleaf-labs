# HLF-P36 · Same result on every machine

**From:** Priya, QA Lead · **About:** 60 min · **Chapter:** Python for Testers · Packages, Virtual Environments & Framework-Ready Code
**Not scored. Unlimited attempts.**

> **The bookshop** is the practice online bookshop that Priya's Tasks use. It is separate from Harbourleaf, the store in the videos, and all of its data is fictional.

> "The practice bookshop's checks need tests that anyone can run: on your laptop, on mine, or in the pipeline. Set the project up properly, write the tests, and leave instructions nobody has to ask about."

## Files in this folder

| File | What it holds |
|---|---|
| `bookshop_checks.py` | The bookshop's checks: `has_price`, `isbn_ok`, `stock_ok`, plus `score_answer` and `payload_lower` |
| `tests/test_bookshop_checks.py` | One example test. Your tests go here. |
| `requirements.txt` | The packages this project needs, pinned |
| `pytest.ini` | Tells PyTest where the tests are, and lets them import `bookshop_checks` |
| `demo/leak_scan/` | Extra practice project (the same one the chapter's examples use) |

Needs **Python 3.10 or later** (pytest 9.1.1).

## Steps

### 1. Your own environment (12 min)
Open this folder in **GitHub Codespaces** (on the repo page: **Code → Codespaces → Create codespace on main**, then `cd labs/pyt06`), or in VS Code on your laptop.

| | Windows (CMD) | macOS / Linux / Codespaces |
|---|---|---|
| Create | `python -m venv .venv` | `python3 -m venv .venv` |
| Activate | `.venv\Scripts\activate` | `source .venv/bin/activate` |

Then in VS Code: Command Palette → **Python: Select Interpreter** → `.venv`.

### 2. Install from the file (8 min)
```
python -m pip install -r requirements.txt
python -m pip list
```
Paste the list.

### 3. Write the tests (20 min)
In `tests/test_bookshop_checks.py`, add 4 tests:
- stock of 0 is allowed
- a negative stock fails
- an ISBN with a letter in it fails
- a missing price fails

Run `python -m pytest -q`.

### 4. Watch one fail (8 min)
Change one test so it expects the wrong result. Run it, paste the failure, and say whether the code or the test is wrong. Then fix it back.

### 5. Your track (7 min)

| Track | Task |
|---|---|
| Test runs | Add a "Setup and run" section to this README with the exact commands for Windows and for macOS/Linux. |
| Model answers | Add 2 tests for `score_answer`: one with the default, one with `case_sensitive=True`. |
| Attack logs | Add a test that `payload_lower` returns `""` when the payload is `None`. |

### 6. Paste your evidence (5 min)
Paste your test file and the final `python -m pytest -q` output into the Task panel in UpModel.

## Hints
- `(.venv)` at the start of the prompt means the environment is active. A new terminal may need activating again.
- `No module named pytest`: this terminal or VS Code isn't using `.venv`.
- Test files are named `test_*.py`, test functions `test_*`, and the check is a plain `assert`.
- On Windows PowerShell, if `activate` is blocked, use **Command Prompt** (CMD) or VS Code's Select Interpreter.
- GitHub Free includes 120 Codespaces core hours and 15 GB storage a month. Stop your codespace when you finish (Codespaces → … → Stop).
