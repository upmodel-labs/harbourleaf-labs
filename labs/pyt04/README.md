# HLF-P34 · One check, one place

**From:** Priya, QA Lead · **About:** 60 min · **Chapter:** Python for Testers · Functions, Modules & Classes
**Not scored. Unlimited attempts.**

> **The bookshop** is the practice online bookshop that Priya's Tasks use. It is separate from Harbourleaf, the store in the videos, and all of its data is fictional.

> "The practice bookshop's three catalogue checks have been pasted into three places, and one copy has already lost two of them. Put each check in one function, and give the results a home."

## Files in this folder

| File | What it holds |
|---|---|
| `starter_pasted_checks.py` | The three checks, pasted three times. Run it, then replace it. |
| `bookshop_catalogue_v1.json` | The bookshop catalogue (40 rows: id, title, category, price, isbn, stock, in_stock) |
| `book_answers.jsonl` | Track *Model answers* |
| `bookshop_attacks.jsonl` | Track *Attack logs* (`en` English, `cy` Welsh) |

## Steps

### 1. Three functions (15 min)
Read `starter_pasted_checks.py`. In a new file `bookshop_checks.py`, write:
- `has_price(book)`: the book has a price
- `isbn_ok(book)`: the ISBN is exactly 13 digits
- `stock_ok(book)`: stock is not negative

Each returns `True` or `False` and has a one-line docstring.

### 2. Import and run (12 min)
In `main.py`, import the three functions, run all three on every row of `bookshop_catalogue_v1.json`, and print each failure with the book id and the check that failed.

### 3. A class for the results (15 min)
In `bookshop_checks.py`, write a class `ShelfReport` with `add(book_id, check, passed)` and `summary()`, which returns the number of checks, the number failed and the failures. Use it in `main.py`.

### 4. Your track (10 min)

| Track | Task |
|---|---|
| Test runs | Give `ShelfReport` a `pass_rate()` method that returns `0.0` for an empty report instead of crashing. |
| Model answers | Write `score_answer(answer, expected, case_sensitive=False)`, where both settings ignore spaces at the ends, and run it on `book_answers.jsonl` twice: with the default, and with `case_sensitive=True`. |
| Attack logs | Write a class `AttackSet` with `add(attack)`, `got_through()` and `by_language()`, and run it on `bookshop_attacks.jsonl`. |

### 5. Paste your evidence (8 min)
Paste `bookshop_checks.py`, `main.py` and the output into the Task panel in UpModel.

## Hints
- A check **returns** its answer; `print` gives the caller nothing (it gets `None`).
- `from bookshop_checks import has_price, isbn_ok, stock_ok, ShelfReport`. Keep both files in this folder.
- Every method takes `self` first. Forget it and Python says `takes 0 positional arguments but 1 was given`.
- Compare with `None` using `is` / `is not`.
