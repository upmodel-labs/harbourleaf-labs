# HLF-P32 · Pass or fail, night by night

**From:** Priya, QA Lead · **About:** 50 min · **Chapter:** Python for Testers · Conditions & Loops: Deciding Pass or Fail
**Not scored. Unlimited attempts.**

> **The bookshop** is the practice online bookshop that Priya's Tasks use. It is separate from Harbourleaf, the store in the videos, and all of its data is fictional.

> "The practice bookshop's search answers were scored on 12 nights against a gate of 46. Sara, the Product Owner, wants pass or fail for each night, and I want the boundary nights handled properly."

## Data

| Night | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Score | 48 | 46 | 45 | 47 | 46 | 44 | 49 | 46 | 45 | 50 | 46 | 47 |

**Gate:** 46 (a night passes at 46 or more).

```python
scores = [48, 46, 45, 47, 46, 44, 49, 46, 45, 50, 46, 47]
gate = 46
```

## Steps

### 1. Pass or fail, night by night (12 min)
Print each night with its score and PASS or FAIL.

### 2. Count and streak (12 min)
Count the nights that passed, and the longest run of passes in a row. Print both with the total number of nights.

### 3. The first failure (8 min)
Use `for … else` to print the first night that failed, or `no failures` if there wasn't one.

### 4. Your track (10 min)
Pick one:

| Track | Task |
|---|---|
| Test runs | The "reserve a copy" check gave **fail**, then **pass**. Retry at most **3** times with `while`, and report honestly. |
| Model answers | Overall **48 of 50** (gate **46**) and the audiobook questions **7 of 10** (gate **8**). Release only if **both** pass. |
| Attack logs | Rows: `blocked`, (empty), `blocked`, `blocked`, `got through`, `blocked`, (empty), `blocked`, `blocked`. Skip the empty rows, give the first row that got through, and count how many got through out of how many ran. |

### 5. Paste your evidence (8 min)
Paste your code and its output, plus the three scores you used to test the boundary.

## Hints
- At the gate is a pass: `>=`, not `>`.
- Test three values around every gate: one below, the gate itself, one above.
- A `while` loop needs something inside it that changes its condition. **Ctrl+C** stops a loop that won't end.
- A loop's `else` runs only if the loop finished without `break`.
