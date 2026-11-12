# Lab lov03 · HLF-P83 · Reading Group Notes: the agent's actions

Part of UpModel, module LLM & Agent Output Validation, chapter 3 (Non-Deterministic & Agentic Behavior Testing).

**Practice data only.** Every name, date and note in these files is made up for teaching. Never paste real or work data into an AI assistant.

## Get the files

The Task needs two folders that sit side by side: `labs/lov03` (this lab) and `labs/_shared` (the shared kit, `lovkit`). Keep `labs` together. Do not copy `lov03` on its own.

**Route 1, free, in your browser (GitHub Codespaces):** open the practice repo on GitHub (`harbourleaf-labs`), choose **Code**, then **Codespaces**, then **Create codespace on main**. Wait until the editor opens, then open a terminal.

**Route 2, on your own computer:** download the whole repo as a ZIP (**Code**, then **Download ZIP**), unzip it, and open a terminal in the unzipped folder.

## What you need

- Python 3.10 or later, and a terminal. On some computers the command is `python3` instead of `python`: use whichever works.
- One package: `pip install pytest`.
- A free AI assistant, for the last step only.
- Nothing else. No model is called and nothing really waits: the assistant and its tools are fakes, and a slow tool is a simulated clock.

## Run the lab

1. In the terminal, go to the lab: `cd labs/lov03/task`.
2. `python -m pytest -q` runs the tests that exist. The first run shows failures and one skipped test: that is the starting point. Not every red test has to turn green: a test that detects a defect in the assistant stays red until the assistant is fixed.
3. `python run_repeated.py` runs the assistant many times and prints each run (step 3). `python run_gate.py --scenario T1` prints the run summary in CI form (your track).

## Folders

| Folder | What it is |
|---|---|
| `task/` | The Task files. Start with `task/notes_brief.md` |
| `demo/` | The files behind the demo recording (Harbourleaf assembly booking). You do not need them for the Task |
| `../_shared/lovkit` | The shared kit: the fake tools and the fake agents |

The reference answers are not in this folder.
