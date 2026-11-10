# taps02 note: start here (practice data only)

## Facts for the steps
- **Title to search for (step 3):** Notes on Waiting
- **Practice order id (step 7, Model answers):** BK-1001
- **HTML snippet (step 7, Attack logs):** `<b>bold</b>`
- **Time limit to use for every wait (step 4 and step 8):** 10 seconds
- The **Add to basket** button on the book page is **disabled until the book has loaded**.
- The help box gives its reply **slowly in slow mode** (1.5 to 3 seconds).

## Locators the note gives you
| Element | Locator |
|---|---|
| Search box (search page) | NAME `q` |
| Search button | CSS `.search-button` |
| First search result | CSS `.result-link` |
| Order box (help page) | ID `order-box` |
| Ask button | CSS `[data-testid='ask-button']` |
| Help reply | CSS `[data-testid='help-reply']` |
| Add to basket button | ID `add-button` |
| Basket lines | CSS `.basket-line` |
| Remove button on a line | CSS `.remove-button` |

## Start the shop
- Normal: `python webshop/server.py`
- Slow and repeatable (steps 1, 4, 8): `python webshop/server.py --slow --seed 7`
- Slow, different each time (step 7, Model answers): `python webshop/server.py --slow`
