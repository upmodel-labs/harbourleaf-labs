# taps03 note: start here (practice data only)

## What changes in version 2 of the shop (step 5)
| | Version 1 | Version 2 |
|---|---|---|
| Search box | label "Search books" | label "Search the shop", and it sits in the header of every page |
| Search button | named "Search" | named "Go" |
| Add button on a book page | named "Add to basket" | named "Add to bag" |
| Everything else (addresses, the basket lines, the Total line, Remove, Place order, the test ids you use for them) | | unchanged |

Start version 1 with `python webshop/server.py` and version 2 with `python webshop/server.py --version v2`. Only one can run at a time, because both use port 8000.

## The values (step 4)
`data/books.json` is your test data, not the shop's own file in `webshop/`. Its shape:

```json
{
  "learning": {"id": "b1", "title": "Learning to Test", "quantity": 2, "total": "Total: 36.00"},
  "queues": {"id": "b3", "title": "Queues and Lines", "quantity": 1},
  "two_book_total": "Total: 39.00",
  "no_match": "Nothing Here"
}
```

The `books` fixture hands the tests this whole structure, so a test reads `books["learning"]["title"]`.

## Elements the starter tests use
| Element | Page | How the tests find it today |
|---|---|---|
| Search box, Search button | search | label and button name (see the table above) |
| Search results | search | `.result-link` |
| Status line | search | `#search-status` |
| Title heading | book | `#book-title` |
| Price | book | test id `book-price` |
| Quantity | book | label "Quantity" |
| Add button | book | button name (see the table above) |
| Basket count in the header | every page | test id `basket-count` |
| Basket lines | basket | `.basket-line` |
| Total line | basket | test id `basket-total` |
| Remove | basket | button named "Remove" (one per line) |
| Place order | basket | button named "Place order" |
| Order status after Place order | basket | test id `order-status` (it holds "placed" once the order is in) |

A page object keeps the locator for the Order status line too, so the journey test can still `expect` on it.

## The order help box (step 6 tracks)
- Page: `/help.html`. Order box test id `order-box`, Ask button test id `ask-button`, reply test id `help-reply`
- While the shop works out an answer, the reply shows "Checking..." and the reply element has no `is-ready` class. When the real answer arrives, the reply text changes and the element gets the class `is-ready` (`#help-reply.is-ready`)
- Your own order, **BK-1001**: one of four wordings, chosen at random. Every wording holds `BK-1001` and the status `shipped`
- **BK-1002** belongs to another customer: one of two refusals. Neither shows the customer's name or a status
- Anything with HTML in it is shown as text
- A very long string: the reply repeats only the first 40 characters, then "..."
