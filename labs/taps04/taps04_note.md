# taps04 note: start here (practice data only)

## The book and the basket (step 2)
- Book: **Learning to Test** (id `b1`), price 18.00. `basket_with_book` adds **2** copies and opens the basket: **Total: 36.00**
- The shop's own book file is `webshop/data/books.json` (keys `id`, `title`, `author`, `price`)

## The shop under parallel runs (steps 2 and 4)
- `worker_id` is `"master"` when the run is not parallel, and `"gw0"`, `"gw1"` and so on under `pytest -n auto`
- Base port **8200**. The `master` and `gw0` workers use 8200, `gw1` uses 8201, and so on: base port plus the worker number
- An address that answers is not proof that it is your shop: `shop_process.py` stops with an error when the shop it started exits at once, for example because an old shop holds the port
- How the tests pick up the address: pytest-playwright reads a fixture called `base_url`, and `page.goto("/")` adds the path to it. `conftest.py` has a `base_url` that returns the hand-started shop on port 8000. In step 2 change it so that it asks for your `shop_server` fixture and returns its address

## The search cases (step 3)
`data/search_cases.csv`: columns `case_id`, `term`, `expected_count`, six rows. The CSV holds only text: convert the count with `int()`.

## The orders page (step 4)
- `/orders.html` lists every order placed since that shop started, as `BK-<number>: <total>`, one `.order` element each. Each shop starts with an empty list
- After Place order the basket page shows `Order BK-<number> placed.` in the element with test id `order-status`. That number tells your order from any other test's order
- Do not call `/api/reset` from a test

## Priya's smoke set (step 5)
The three journeys that run on every push:
1. Search to basket: `test_search_to_basket_journey` in `tests/test_journeys.py`
2. The basket total for two copies: `test_total_for_two_copies` in `tests/test_basket.py`
3. The help box says the order is shipped: `test_help_box_says_the_order_is_shipped` in `tests/test_help_box.py`

## The pipeline (step 6)
- The supplied workflow runs the shop a little slower than your Codespace does, to stand for a slower build machine
- The first push is red by design. `test_help_box_says_the_order_is_shipped` passed in your Codespace and fails in the smoke job. Read the report and the trace to find out why
- The fix this Task allows is **one changed line in that test**, and nothing else. Do not re-run hoping for green
- The `full` job starts on a pull request into `main` in your own fork

## The help box (step 7 tracks)
- `support/reply_check.py` types an order number into the help box and checks the reply against one row: every word in `must_hold` is there, no word in `must_not_show` is, and typed markup comes back as text
- `data/help_replies.csv` columns: `reply_id`, `typed`, `must_hold`, `must_not_show` (words separated by `|`)
- Meera: the first five rows. Brian: `data/misuse_cases.csv`, three rows: another customer's order number (BK-1002), a piece of HTML, a very long string (the reply repeats only the first 40 characters)
