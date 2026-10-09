# HLF-P31 · Your first run summary

**From:** Priya, QA Lead · **About:** 45 min · **Chapter:** Python for Testers · Python Setup & First Script for Testers
**Not scored. Unlimited attempts.**

> **The bookshop** is the practice online bookshop that Priya's Tasks use. It is separate from Harbourleaf, the store in the videos, and all of its data is fictional.

> "The practice bookshop's nightly checks have finished: 120 checks, 9 failed, 3 skipped. Nobody should count that by hand again. Write the script that prints the summary, and tell me which pass rate I should report."

## Steps

### 1. Set up and prove it (8 min)
Use **VS Code**, **PyCharm** or **Google Colab**. Run this and paste the line it prints:

| Where | Command |
|---|---|
| Windows terminal | `python --version` |
| macOS / Linux terminal | `python3 --version` |
| Colab cell | `!python --version` |

### 2. The summary (20 min)
Create `bookshop_summary.py` (or a Colab cell).
- Store the numbers in variables: **120** checks, **9** failed, **3** skipped.
- Let Python work out how many checks were **executed** and how many **passed**. Don't work them out by hand.
- Print both pass rates to **one decimal place**: of the checks **executed**, and of **all** checks.
- Answer in one sentence: which rate should Priya report, and why?

### 3. Who ran it (5 min)
Ask for the tester's name with `input()` and put it in the first line of the summary.

### 4. Your track (7 min)
Pick one and print it the same way:

| Track | Numbers |
|---|---|
| Test runs | Checkout checks: **64** run, **5** failed |
| Model answers | Book search: **44** of **50** correct, gate **46** (the pass mark) |
| Attack logs | **18** attacks, **1** got through |

### 5. Paste your evidence (5 min)
Paste your script and its output into the Task panel in UpModel.

## Hints
- `/` always gives a decimal result; `//` drops the fraction.
- `f"{rate:.1f}%"` prints a number with one decimal place.
- `TypeError: can only concatenate str (not "int") to str` means text was joined to a number: use an f-string.
- Stuck? Paste your output into the AI Tutor.
