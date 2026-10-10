# starter_pasted_checks.py - the same three checks, pasted into three places.
# Your Task: turn them into functions in bookshop_checks.py and call them from main.py.
import json

with open("bookshop_catalogue_v1.json", encoding="utf-8") as f:
    books = json.load(f)

# copy 1: the nightly catalogue check
for book in books:
    if book.get("price") is None:
        print(book["id"], "no price")
    if not (len(book["isbn"]) == 13 and book["isbn"].isdigit()):
        print(book["id"], "bad ISBN")
    if book["stock"] < 0:
        print(book["id"], "negative stock")

# copy 2: pasted into the reservations report (look closely: is every check here?)
for book in books:
    if book["in_stock"]:
        if book.get("price") is None:
            print(book["id"], "no price (in stock)")
        if not (len(book["isbn"]) == 13 and book["isbn"].isdigit()):
            print(book["id"], "bad ISBN (in stock)")

# copy 3: pasted again for the children's shelf, and two checks were left out
for book in books:
    if book["category"] == "children":
        if book.get("price") is None:
            print(book["id"], "no price (children)")
