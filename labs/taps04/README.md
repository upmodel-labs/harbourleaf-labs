# taps04: fast, independent, in the pipeline (HLF-P64)

Practice data only. The shop runs on your own machine or Codespace. Only ever test the shop you started yourself.

You work in **your own fork** of the practice repo. Every command runs from this folder (`labs/taps04`). The one file outside it is the pipeline file in step 6: `.github/workflows/taps04-tests.yml`, at the root of the repo.

Start with `taps04_note.md`. It holds the book, the search cases, the smoke journeys, the ports and the rules this Task refers to. Write your answers in `taps04_answers.md`.

## In a GitHub Codespace (the main way)

Create the Codespace from your fork. It installs the requirements and Chromium for you. If `pytest --version` fails:

```bash
cd labs/taps04
pip install -r requirements.txt
python -m playwright install --with-deps chromium
```

Step 1: terminal 1 starts the shop by hand, terminal 2 runs the tests.

```bash
python webshop/server.py        # terminal 1: shop version 1 on port 8000
pytest                          # terminal 2
```

From step 2 a fixture starts the shop for you, so stop the shop in terminal 1 first (Ctrl+C).

## On your laptop (fallback)

You need Python 3.10 or newer and git.

```bash
cd labs/taps04
python -m venv .venv
# Windows: .venv\Scripts\activate      Mac or Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

Step 6 (the pipeline) needs your fork on GitHub either way.

## Files

| File | Used in |
|---|---|
| `taps04_note.md`, `taps04_answers.md` | every step |
| `conftest.py` | steps 2 and 4 (supplied with the page-object fixtures; you add three fixtures and one more) |
| `shop_process.py` | step 2 (supplied: `start_shop`, `stop_shop`) |
| `tests/test_basket.py` | steps 2 and 5 |
| `tests/test_search_copies.py`, `search_tests_before.py`, `data/search_cases.csv` | steps 3 and 8 (leave `search_tests_before.py` alone) |
| `tests/test_orders.py` | step 4 |
| `tests/test_journeys.py`, `tests/test_help_box.py` | steps 5 and 6 |
| `pytest.ini` | step 5 |
| `support/reply_check.py`, `data/help_replies.csv`, `data/misuse_cases.csv` | step 7 (your track) |
| `pages/` | the page objects from chapter 3 |
| `webshop/` | the practice shop (version 1) |
