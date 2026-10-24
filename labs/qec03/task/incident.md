# Incident: the saving after the offer ended

**Fictional practice data.** Times are store time.

## What happened
- The offer ended at **20:00:00 on 30 November**.
- Between 20:00:00 and 23:59:59, **37 orders** were given a free paperback.
- The saving stopped at **00:00 on 1 December**, when the daily cache refreshed.
- It was found at **10:15 on 1 December**, in the daily orders report.

## Facts the team found
1. The offer rules service stopped giving the saving at 20:00:00, as intended. Its tests had been updated for the new end time in October, and they passed.
2. The cart page does not ask the offer rules service whether the offer is active. It reads a copy from a **daily cache**.
3. The daily cache is refreshed **once a day, at 00:00**. At 00:00 on 30 November the offer was active, so the cache said "active" until 00:00 on 1 December.
4. Checkout takes the saving from the cart.
5. The daily cache also holds **the free-delivery threshold** and **the featured-books list**.
6. The end-time change in October went through the team's **change checklist**. The checklist asks for: the rule, its tests, the cart message and the release note. It has no question about other places that hold a copy of the value.
7. The developer who made the change did not know that the cart read a cached copy. The cache and its refresh time are not written down in any document.
8. The test environment **clears the cache on every deploy**, so the tests always read a fresh value.
9. No alert checks for orders that get the saving after the offer has ended. The daily orders report is read the next morning.
10. The requirement says: "The saving must not apply to any order placed after the end time."
