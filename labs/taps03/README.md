# taps03: one change, one place (HLF-P63)

Practice data only. The shop runs on your own machine. Only ever run the tests against the practice shop you started yourself.

Start with `taps03_note.md`. It holds what changes in version 2 of the shop and the values this Task refers to.

## In a GitHub Codespace (the main way)

Open the practice repo in a Codespace, then in the first terminal:

```bash
cd labs/taps03
pip install -r requirements.txt
python -m playwright install --with-deps chromium
```

The second command takes a few minutes. Open a second terminal and start shop version 1:

```bash
cd labs/taps03
python webshop/server.py
```

To see the shop in a browser, open port 8000 from the Ports tab. Back in the first terminal:

```bash
pytest
```

You should see `8 passed`. No browser window opens: the run is headless.

Version 2 of the shop uses the same port, so stop version 1 with Ctrl+C first, then run `python webshop/server.py --version v2`.

## On your laptop (fallback)

You need Python 3.10 or newer and git.

```bash
cd labs/taps03
python -m venv .venv
# Windows: .venv\Scripts\activate      Mac or Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
python webshop/server.py          # leave this running, then open a second terminal in labs/taps03
pytest
```

## Searching your tests

| | Mac, Linux, Codespaces | Windows (Command Prompt) |
|---|---|---|
| Step 2: every locator and the address | `grep -n "get_by_\|locator(\|goto\|localhost" tests/*.py` | `findstr /n /c:"get_by_" /c:"locator(" /c:"goto" /c:"localhost" tests\*.py` |
| Step 3: nothing should print | `grep -n "get_by_\|locator(\|goto\|click(" tests/*.py` | `findstr /n /c:"get_by_" /c:"locator(" /c:"goto" /c:"click(" tests\*.py` |

## Files

| File | Used in |
|---|---|
| `taps03_note.md` | every step |
| `tests/` | steps 1 to 5: four files, two flat tests each (the suite you rearrange) |
| `layers.md` | steps 2, 4 and 5 |
| `pages/` | step 3 (empty for now: only `__init__.py`) |
| `data/books.json` | step 4 (supplied, pre-filled) |
| `conftest.py`, `pytest.ini` | supplied, you read them in step 4 |
| `originals/` | untouched copies of the starter `test_search.py` and `test_basket.py` (step 7) |
| `saved_pages/v1/` | the three pages as saved from version 1 (steps 3 and 7) |
| `ai_version/` | step 7: its own `conftest.py`, `pytest.ini` and `data/books.json` |
| `webshop/` | the practice shop |

The starter tests write the full address in every test, so plain `pytest` works in step 1. From step 3 the address comes from the command line (`--base-url http://localhost:8000`), and from step 4 from `pytest.ini`.
