# taps01: first browser checks for the practice bookshop (HLF-P61)

Practice data only. The shop runs on your own machine. Only ever test the shop you started yourself.

Start with `taps01_note.md`. It holds the journey facts, the six elements, the practice order ids and the status for your order.

## In a GitHub Codespace (the main way)

Open the practice repo in a Codespace, then in the first terminal:

```bash
cd labs/taps01
pip install -r requirements.txt
python -m playwright install --with-deps chromium
```

The second command takes a few minutes. Open a second terminal:

```bash
cd labs/taps01
python webshop/server.py
```

To see the shop in a browser, open port 8000 from the Ports tab. Back in the first terminal:

```bash
pytest test_shop_opens.py
```

You should see `1 passed`. No browser window opens: the run is headless.

## On your laptop (fallback)

You need Python 3.10 or newer.

```bash
cd labs/taps01
python -m venv .venv
# Windows: .venv\Scripts\activate      Mac or Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
python webshop/server.py          # leave this running, then open a second terminal in labs/taps01
pytest test_shop_opens.py
```

## Files

| File | Used in |
|---|---|
| `taps01_note.md` | every step |
| `test_shop_opens.py` | step 1 (supplied, passes) |
| `test_scratch.py`, `locators.md` (you write it) | step 2 |
| `test_basket.py` | step 3 |
| `test_checkout_broken.py` | step 4 (supplied, fails on purpose, leave it as it is) |
| `test_help_box.py` | step 5 |
| `help_replies.csv`, `test_attack.py` | step 6 (your track) |
| `search_page.html`, `book_page.html`, `basket_page.html` | step 7 |
| `webshop/` | the practice shop |

pytest.ini sets the base URL, `http://localhost:8000`, so tests open pages with short paths such as `page.goto("/")`.
