# Lab lov05 · HLF-P85 · Reading Group Notes: probe the assistant

Part of UpModel, module LLM & Agent Output Validation, chapter 5 (Adversarial Testing & Prompt Injection Basics).

**Practice data only.** Every name, date and note in these files is made up for teaching. Never paste real or work data into an AI assistant. **Test material here is a payload class tag, never attack text.**

## Get the files

Keep the `labs` folder together: the shared kit (`labs/_shared`) sits beside this lab, and this lab does not use it. Do not copy `lov05` on its own.

**Route 1, free, in your browser (GitHub Codespaces):** open the practice repo on GitHub (`harbourleaf-labs`), choose **Code**, then **Codespaces**, then **Create codespace on main**. Wait until the editor opens, then open a terminal.

**Route 2, on your own computer:** download the whole repo as a ZIP (**Code**, then **Download ZIP**), unzip it, and open a terminal in the unzipped folder.

## What you need

- Python 3.10 or later, and a terminal. On some computers the command is `python3` instead of `python`: use whichever works.
- One package: `pip install pytest`.
- A free AI assistant, for the last step only.
- Nothing else. The assistant is a fake: nothing is sent anywhere and nothing can reach a real system.

## Run the lab

1. In the terminal, go to the lab: `cd labs/lov05/task`.
2. `python -m pytest -q` runs the tests that exist. The first run shows failures: that is the starting point. Not every red test has to turn green: a test that detects what the assistant did stays red until the assistant is fixed.
3. `python reply_check.py` (step 5) and `python run_regression.py` (your track) are scripts you run from the same folder.

## Folders

| Folder | What it is |
|---|---|
| `task/` | The Task files. Start with `task/notes_brief.md` |
| `../_shared/lovkit` | The shared kit (this lab does not need it) |

The reference answers are not in this folder.
