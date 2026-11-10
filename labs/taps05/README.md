# taps05: same journey, two more languages (HLF-P65)

Practice data only. The shop runs on your own Codespace or machine. Only ever run these tests against the shop you started yourself.

Start with `transfer_note.md`. Write your answers in `notes.md`.

## In a GitHub Codespace (the main way)

Open the practice repo in a Codespace. Python, Node and Java with Maven are installed there.

Terminal 1, in `labs/taps05`. Leave it running:

```bash
python webshop/server.py
```

Terminal 2, TypeScript:

```bash
cd ts
npm ci
npx playwright install --with-deps chromium
npx playwright test
```

You should see `1 passed`. Terminal 2, Java:

```bash
cd ../java
mvn -q test
```

The first run downloads the Java libraries and, for Selenium, a matching driver, so it takes a few minutes. A quiet run with no `BUILD FAILURE` is a pass. Terminal 2, Python (install only; the Python quick check runs in step 6):

```bash
cd ../python_reference
pip install -r requirements.txt
python -m playwright install --with-deps chromium
```

## On your laptop (fallback)

You need Python 3.10 or newer, Node 20 or newer, Java 17 or newer, Maven 3.9 or newer, and Chrome installed. Run the same commands. Check them with `python --version`, `node --version`, `java -version` and `mvn -v`.

## If a run fails

| What you see | The usual cause |
|---|---|
| `ECONNREFUSED` or "connection refused" at `localhost:8000` | The shop is not running. Start it in terminal 1 |
| "Address already in use" when starting the shop | An old shop still holds port 8000. Stop it with Ctrl+C in its terminal |
| `npx playwright test` says the browser is missing | Run `npx playwright install --with-deps chromium` in `ts` |
| `mvn: command not found` or "release version 17 not supported" | Maven or Java 17 or newer is missing. Check `mvn -v` and `java -version` |
| `SessionNotCreatedException` in Java | The driver and Chrome do not match. Run the test again: Selenium Manager fetches a matching driver. On a laptop, update Chrome |

## Files

| File | Used in |
|---|---|
| `transfer_note.md`, `notes.md` | every step |
| `python_reference/` | steps 3, 6 and 7: `test_search.py`, `test_help_box.py`, `search_page.html` (the two Python tests, both marked smoke) |
| `ts/` | steps 2, 3 and 6: `tests/basket.spec.ts`, `pages/BasketPage.ts`, a starter `tests/search.spec.ts` |
| `java/` | steps 4 and 6: `BasketTest.java`, `MisuseTest.java` |
| `transfer_map.csv` | step 5 |
| `webshop/` | the practice shop (version 1) |
