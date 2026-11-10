# The practice bookshop's web shop

A tiny web shop made only for the test-automation-python-stack labs (HLF-P61 to HLF-P65). It holds no real data and is not connected to anything. It is the practice bookshop, separate from Harbourleaf. Every learner runs their own copy inside their own Codespace.

This is the practice shop for this lab. Start it, test it, and leave its files as they are.

## Start it

```bash
python webshop/server.py                 # v1 on http://localhost:8000
python webshop/server.py --version v2    # v2 (chapter 3)
python webshop/server.py --slow          # answers take 1.5 to 3 s (chapter 2: why fixed sleeps fail)
python webshop/server.py --seed 7        # repeatable wording and delays
```

Python 3.10 or newer. Standard library only, so there's nothing to install for the shop itself. In Codespaces, open the **Ports** tab to view it in a browser.

## Pages and what each lab uses

| Page | What is on it | Used by |
|---|---|---|
| `/` search | Search box (label "Search books", `name="q"`), Search button (`.search-button`), results list (`.result-link`), status line. `/?q=word` searches straight away | ch1 to ch5 |
| `/book.html?id=b1` | Title, author, price, Quantity (1 to 10), **Add to basket** (disabled until the book has loaded), "Added to basket." status | ch1 to ch5 |
| `/basket.html` | One row per book (`.basket-line`), **Remove** (redraws every row, so old Selenium handles go stale), `Total: 36.00`, **Place order** | ch1 journey, ch2 stale element, ch3, ch4 |
| `/help.html` | The order help box: Order number, Ask, "You asked about: ..." and the reply | ch1 step 5, every Model answers and Attack logs track |
| `/orders.html` | Every order placed since the server started: **one shared list for all tests** | ch4 step 4 (a test that only passes after another) |

The basket lives in the browser (`localStorage`), so each Playwright test starts with an empty basket. The order list lives in the server and is shared on purpose. `POST /api/reset` empties it.

## The order help box

| You type | The reply |
|---|---|
| `BK-1001` (your order) | One of four wordings, chosen at random. It always holds `BK-1001` and the status `shipped`. Your other orders: `BK-1003` delivered, `BK-1004` cancelled |
| `BK-1002` (another customer's order) | One of two refusals. It never shows the customer's name or the status |
| An unknown number | One of three "can't find" wordings. It repeats at most 40 characters of what you typed |
| Anything with HTML in it | Shown as text, never as a new element |

Statuses used: placed, packed, shipped, out for delivery, delivered, cancelled. The data is in `data/orders.json`, and the books are in `data/books.json` (8 books, plain prices, no currency).

## v1 and v2 (chapter 3)

| | v1 | v2 |
|---|---|---|
| Search box | In the page, label "Search books", button "Search", test ids `search-box` and `search-button` | Moved to the header on every page, label "Search the shop", button "Go", test ids `search-input` and `search-go` |
| Basket word | basket: "Add to basket", "Basket (n)", test id `add-to-basket` | bag: "Add to bag", "Bag (n)", test id `add-to-bag` |
| Addresses, element ids and the help box | unchanged | unchanged |

## Rules kept

- One stylesheet (`static/shop.css`) and one script (`static/shop.js`) for every page and both versions. No inline styles, no inline scripts.
- Text from the server or the learner is always written with `textContent`.
- No real brands, people or data. The banner on every page says it is a practice shop.


