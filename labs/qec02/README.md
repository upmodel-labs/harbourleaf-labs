# labs/qec02 · Quality Engineering Core · chapter 2 · Regression and smoke suites

Practice files for the chapter 2 demo and Task HLF-P52 (*Bundle & Save regression kit*, about 70 min). **Not scored. Unlimited attempts.** Everything here is fictional.

> **The bookshop** is the practice online bookshop that Priya's Tasks use. It is separate from Harbourleaf, the store in the videos.

## You need
- **Python 3.10 or later** and a terminal. Work on your laptop in VS Code, or in GitHub Codespaces (`cd labs/qec02/task`).
- Install PyTest from the file in the folder you are working in:
  - Windows (CMD): `python -m venv .venv` then `.venv\Scripts\activate`
  - macOS / Linux / Codespaces: `python3 -m venv .venv` then `source .venv/bin/activate`
  - then `python -m pip install -r requirements.txt`
- A notes file or a spreadsheet for your answers.

## Files

| Folder | What it holds |
|---|---|
| `task/` | Task HLF-P52. `bundle_regression_note.md` (start here), `areas.csv`, `dependencies.csv`, `tests/` (30 PyTest tests), `pytest.ini`, `nightly_runs.csv`, `builds.csv`, `offer_messages_set.csv`, `double_labelled.csv`, `baseline.json`, `run_1.json` to `run_3.json`, `scorer.py` |
| `demo/` | The files used in the chapter's demo video: a small Room Match suite with 40 tests (`tests/`, `stock.py`, `stock_new.py`, `change_note.md`) and `scorer/` |
| `scorer.py` | The lab scorer (a copy sits in `task/` and in `demo/scorer/`). Standard library only. |

## The scorer

Run these from the folder that holds `scorer.py` and the files (for the Task: `labs/qec02/task`).

```
python scorer.py fitness offer_messages_set.csv --baseline baseline.json --stale-before 2026-10-14
python scorer.py agree double_labelled.csv --bar 90
python scorer.py compare --baseline baseline.json --runs run_1.json run_2.json run_3.json
python scorer.py baseline --runs run_1.json run_2.json run_3.json --tolerance 0.05 --out new_baseline.json
```

| Command | What it does |
|---|---|
| `fitness <set.csv>` | One line per check: duplicates, slice sizes against the 10 and 30 rule, set version against the baseline's, labels older than a date, coverage against recent traffic. Each line is OK, FLAG or SKIPPED. Options: `--baseline`, `--stale-before`, `--traffic`. |
| `agree <double.csv>` | Agreements out of the sample, the percentage, and PASS or FAIL against the bar (`--bar`, default 90). |
| `compare` | Checks that the model and the set version match the baseline's, then prints the mean of the runs, the line (baseline minus tolerance) and PASS or WORSE. It stops with a message if the set versions differ. |
| `baseline` | Takes the mean of 3 to 5 runs as a new baseline and writes it, with the prompt, model and set versions, to `--out`. |

## Useful PyTest commands

```
pytest                       run every test
pytest -m smoke              run the tests marked smoke
pytest -m "not quarantine"   everything except quarantined tests
pytest -k "cart or fees"     tests whose names match
pytest --lf                  only what failed last time
```

`pytest.ini` registers the markers `smoke`, `quarantine` and `misuse`, and runs with `--strict-markers`, so a mistyped marker is an error.

## How to work
1. Read `task/bundle_regression_note.md`, then work through the Task steps in UpModel in order. Give a reason for every choice.
2. Practice files only for the AI step, never real or work data.
3. Fork the repo (top right) to keep your own copy of your work.
