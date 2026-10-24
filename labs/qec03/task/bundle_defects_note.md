# Bundle & Save: defects and the last evening

**The practice bookshop.** Separate from Harbourleaf. Fictional data.

## How the offer works
- **Buy any 3 paperbacks, and the cheapest is free.** Hardbacks and other formats do not count towards the 3.
- The cart works out the saving and shows it. **Checkout takes the saving from the cart; it does not work it out again.**
- The first run of the offer ended at **20:00:00 store time on 30 November** (moved from 23:59:59 in October).
- **The offer comes back for a second run from Monday 7 December.** The next release is on **Thursday 3 December**: anything that must be right for the second run has to be fixed and re-tested in it.
- About **1 in 8** carts of 3 or more books holds a hardback.
- **The wishlist shows no prices or savings.** That is by design: prices are shown on the book page and in the cart.

## The defect list (`defects.csv`)
- 18 defects raised during and just after the first run. Columns: id, title, component, symptom, severity, status, found_in, reopened, opened.
- **Six have status `new`**: they are waiting for triage.
- The bookshop's **product owner** decides priority and accepts any deferral in writing.

## The last evening (`incident.md`)
On the last evening of the first run, the saving kept being given after 20:00:00. `incident.md` has the facts, and what the daily cache holds.
