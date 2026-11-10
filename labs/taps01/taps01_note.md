# taps01 note: start here (practice data only)

## The journey (step 3)
1. Start on the search page.
2. Search for the title: **Learning to Test**
3. Open that book from the results.
4. Set the quantity to **2**.
5. Add it to the basket, then open the basket.

Expected in the basket (assert all three):
- Number of lines: **1**
- Quantity on the line: **2**
- Total text: **Total: 36.00**

Locators the note gives you (you do not choose these):
- Basket lines: `.basket-line`
- The quantity on a line: `.line-qty`

## The six elements (step 2)
Find each locator yourself. These elements also carry a test id:

| Element | Page | Test id |
|---|---|---|
| Search box | search | `search-box` |
| Search button | search | `search-button` |
| Search result for "Learning to Test" | search (after a search) | none |
| Quantity | book | `quantity` |
| Add to basket button | book | `add-to-basket` |
| Basket total | basket | `basket-total` |

## Practice orders (step 5)
- **BK-1001** is your order. Its status is **shipped**.
- BK-1002 belongs to another customer, **Tomas**. The help box must never show his name or his status.
- BK-1003 is delivered. BK-1004 is cancelled.

## Saved pages (step 7)
`search_page.html`, `book_page.html` and `basket_page.html` are the three pages as the journey shows them.
