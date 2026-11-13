# Lab lov04 · HLF-P84 · Reading Group Notes: guard the summary

Part of UpModel, module LLM & Agent Output Validation, chapter 4 (AI Guardrails & Confidence Scoring).

**Practice data only.** Every name, date and note in these files is made up for teaching. Never paste real or work data into an AI assistant.

## Get the files

Keep the `labs` folder together: the shared kit (`labs/_shared`) sits beside this lab, and this lab uses only its own practice data. Do not copy `lov04` on its own.

**Route 1, free, in your browser (GitHub Codespaces):** open the practice repo on GitHub (`harbourleaf-labs`), choose **Code**, then **Codespaces**, then **Create codespace on main**. Wait until the editor opens, then open a terminal.

**Route 2, on your own computer:** download the whole repo as a ZIP (**Code**, then **Download ZIP**), unzip it, and open a terminal in the unzipped folder.

## What you need

- Python 3.10 or later, and a terminal. On some computers the command is `python3` instead of `python`: use whichever works.
- Two packages: `pip install pytest pydantic`.
- A free AI assistant, for the last step only.
- Nothing else. No model is called: the guards are small pieces of plain Python.

## Run the lab

1. In the terminal, go to the lab: `cd labs/lov04/task`.
2. `python -m pytest -q` runs the tests that exist. The first run shows failures and one skipped test: that is the starting point. Not every red test has to turn green: a test that detects a defect in a guard stays red until the guard is fixed.
3. `python threshold.py` prints the threshold table (step 4). `python refusal_count.py` prints the refusal list (step 6). `python run_gate.py --scenario T1` runs the fail-safe check as a build check (continuous integration, CI) (your track).

## Folders

| Folder | What it is |
|---|---|
| `task/` | The Task files. Start with `task/notes_brief.md` |
| `../_shared/lovkit` | The shared kit (this lab uses only its fixed practice data) |

The reference answers are not in this folder.
