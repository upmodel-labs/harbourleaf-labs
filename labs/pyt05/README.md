# HLF-P35 · Make it fail loudly

**From:** Priya, QA Lead · **About:** 50 min · **Chapter:** Python for Testers · Errors, Exceptions & Debugging
**Not scored. Unlimited attempts.**

> **The bookshop** is the practice online bookshop that Priya's Tasks use. It is separate from Harbourleaf, the store in the videos, and all of its data is fictional.

> "The practice bookshop's scoring script crashes on its own data, and I don't trust its average even when it runs. Make every bad row visible, then find the bug."

## Files in this folder

| File | What it holds |
|---|---|
| `bookshop_score.py` | The scoring script. It crashes, and it has one bug that isn't a crash. |
| `search_scores.jsonl` | 30 review scores (0 to 5) for the bookshop's search answers. Three rows are bad. |
| `empty_run.csv` | Track *Test runs*: a run where no checks ran (header only) |
| `bookshop_attacks_v2.jsonl` | Track *Attack logs*: one attack has no payload |
| `demo/` | The file used in the chapter's demo |

The gate: the **average score must be at least 4.0**.

## Steps

### 1. Read the crash (7 min)
Run `bookshop_score.py`. Write down the error type, the message and the line of the script that raised it.

### 2. Handle each bad row (15 min)
`search_scores.jsonl` has three bad rows. Catch each with the **right** `except` (no `except Exception`, no `pass`), record the line number and the reason, and carry on. Print how many rows were read, how many were scored, and the error list.

### 3. Find the bug with the debugger (12 min)
The average still looks wrong.
1. In VS Code, click the margin left of a line inside the loop to set a breakpoint (or press **F9**).
2. Start **Run and Debug** (**F5**) → *Python Debugger: Debug Python File*.
3. Add `total` and `score` to **WATCH**. Step with **F10**.
4. When you see the bug, take a screenshot of the WATCH panel. Then fix it.

### 4. Your track (8 min)

| Track | Task |
|---|---|
| Test runs | Work out the pass rate for `empty_run.csv`. It has no checks, so make the script say so instead of crashing. |
| Model answers | Make the report say "scored X of Y" and list every row that couldn't be scored, with its reason. |
| Attack logs | Print each payload in `bookshop_attacks_v2.jsonl` in lower case. One has no payload: record it by id instead of crashing. |

### 5. Defect note (8 min)
Write 4 lines on the bug from step 3: what's wrong, where, the effect on the result (old vs new average, against the gate of 4.0), and the fix.

## Hints
- Read a traceback from the **bottom**: the last line is what went wrong, the line above is where.
- A `JSONDecodeError`'s "line … column …" counts inside the text you gave `json.loads`, not your file. Keep your own line counter.
- Put the `try` around **one row**, not the whole loop, so one bad row can't stop the rest.
