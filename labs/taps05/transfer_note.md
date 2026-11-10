# taps05 note: start here (practice data only)

## The shop
- Address: `http://localhost:8000` (start it with `python webshop/server.py` in `labs/taps05`; it is version 1)
- Only ever run these tests against the shop you started yourself

## The journey values
- Book: **Learning to Test** (id `b1`), price 18.00
- Quantity **2** gives **Total: 36.00**
- Search word for the Java search test (step 4): **Percentiles**. The first result is the book **A Small Guide to Percentiles**

## Locators for the Java search test
- Search box: `By.name("q")`
- Search button: `By.className("search-button")`
- Results: `By.cssSelector(".result-link")`

## The order help box
- Page `/help.html`. Order number box (test id `order-box`), Ask button (test id `ask-button`), reply (test id `help-reply`, also `#help-reply`)
- The reply is worded one of several ways, chosen at random. Check what must hold, never one exact sentence
- Your own order: **BK-1001**, status shipped

## The three misuse inputs (Attack logs track)
1. Another customer's order number: **BK-1002**. Its owner is **Tomas**. The reply must never show that name or the order's status
2. A piece of HTML: `<b>bold</b>`. The shop must show it as text and never create a `b` element
3. A very long string. The reply repeats at most 40 characters of what was typed, so the part beyond the 40th character must never appear in the reply. (The line "You asked about: ..." above the reply echoes the whole input, which is why the helper reads only the reply area.)
