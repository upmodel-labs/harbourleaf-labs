# layers.md: where each repeat should live

## Step 2: the address
The address `http://localhost:8000` is written ___ times, in ___ of the four test files. Source:

## Step 2: the locators
| What it finds | Times in the eight tests | Which files |
|---|---|---|
| Search box (label) | | |
| Search button | | |
| Search results | | |
| Status line (search) | | |
| Title heading | | |
| Price | | |
| Quantity | | |
| Add button | | |
| Basket count | | |
| Basket lines | | |
| Total line | | |
| Remove | | |
| Place order | | |
| Order status | | |

## Step 2: the target folders
- tests/:
- pages/:
- config:
- data/:

## Step 4: what each fixture gives a test
- search_page:
- book_page:
- basket_page:
- books:

Why plain `pytest` failed with the base_url line commented out, in one line:

## Step 5: the two counts
- After (from `git diff --stat`): ___ files, ___ lines changed.
- Before (from my step 2 table): the old suite would have needed ___ places edited, in ___ test files.

What the two counts show, in one sentence:
