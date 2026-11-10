# taps02: mend the inherited Selenium suite (HLF-P62)

Practice data only. The shop runs on your own machine. Only ever test the shop you started yourself.

Start with `selenium_note.md`. It holds the title to search for, the practice order id, the HTML snippet, the time limit, the locators and the shop start commands.

## In a GitHub Codespace (the main way)

Open the practice repo in a Codespace, then in the first terminal:

```bash
cd labs/taps02
pip install -r requirements.txt
```

The first Selenium run takes longer, because Selenium Manager fetches the driver and Chrome for Testing. Open a second terminal and start the shop:

```bash
cd labs/taps02
python webshop/server.py
```

To see the shop in a browser, open port 8000 from the Ports tab. Back in the first terminal, run the old suite once:

```bash
python -m pytest old_suite -v
```

No browser window opens: the run is headless. One test fails even on the normal shop. That is expected: it is the stale element in step 5.

To run the shop slowly, stop it (Ctrl+C) and start it again:

```bash
python webshop/server.py --slow --seed 7
```

Answers then take 1.5 to 3 seconds, the same each time. Without `--seed` the delay and the wording of the help reply change between runs.

## On your laptop (fallback)

You need Python 3.10 or newer and Chrome installed.

```bash
cd labs/taps02
python -m venv .venv
# Windows: .venv\Scripts\activate      Mac or Linux: source .venv/bin/activate
pip install -r requirements.txt
python webshop/server.py          # leave this running, then open a second terminal in labs/taps02
python -m pytest old_suite -v
```

For step 6 you also need Playwright's browser: `python -m playwright install chromium`.

## Files

| File | Used in |
|---|---|
| `selenium_note.md` | every step |
| `taps02_note.md` | steps 1, 6 and 7 |
| `conftest.py` | supplies the `driver` fixture (read it in step 1) |
| `old_suite/` | steps 1, 2, 4 and 5 (six tests) |
| `suite_review.md` | steps 2, 4 and 5 |
| `test_search.py` | step 3 |
| `originals/` | untouched copies of two old tests, for step 8 |
| `compare/ch1_test_basket.py` | step 6, if you do not have your chapter 1 file |
| `track_pipeline/`, `track_attack/`, `track_meera/` | step 7 (your track) |
| `saved_pages/book_page.html`, `saved_pages/help_page.html` | step 8 |
| `ai_version/` | step 8 (save the AI's two files here) |
| `webshop/` | the practice shop |

`pytest.ini` points pytest at `old_suite` by default, so run the other folders by name, for example `python -m pytest track_pipeline -v`.
