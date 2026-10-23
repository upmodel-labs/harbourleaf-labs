"""The practice bookshop's Bundle & Save offer (fictional; for the qec02 lab).

Offer: with 3 paperbacks in the cart, the cheapest one is free; with 6, the two cheapest.
Hardbacks never count. The offer ends at END_TIME, store time.
"""
from datetime import datetime

END_TIME = datetime(2026, 11, 30, 23, 59, 59)
TAX_RATE = 0.05
CAMPAIGN_ACTIVE = True          # the catalogue badge reads this flag, not the clock

BOOKS = [
    {"title": "The Salt Road", "format": "paperback", "price": 12.99},
    {"title": "Quiet Harbour", "format": "paperback", "price": 9.99},
    {"title": "Paper Kingdoms", "format": "paperback", "price": 14.99},
    {"title": "The Last Ferry", "format": "hardback", "price": 24.99},
    {"title": "Glass Country", "format": "hardback", "price": 27.50},
    {"title": "Moth and Lamp", "format": "paperback", "price": 8.99},
]

USERS = {"asha": {"password": "pw-asha-1", "orders": ["o-1001", "o-1007", "o-1012"]}}


def paperbacks(cart):
    return [b for b in cart if b["format"] == "paperback"]


def offer_is_on(now):
    return now <= END_TIME


def free_books(cart, now):
    """The free paperbacks: the cheapest one in every full set of three."""
    if not offer_is_on(now):
        return []
    books = sorted(paperbacks(cart), key=lambda b: b["price"])
    return books[: len(books) // 3]


def saving(cart, now):
    return round(sum(b["price"] for b in free_books(cart, now)), 2)


def subtotal(cart):
    return round(sum(b["price"] for b in cart), 2)


def total(cart, now):
    return round(subtotal(cart) - saving(cart, now), 2)


def total_with_tax(cart, now):
    return round(total(cart, now) * (1 + TAX_RATE), 2)


def cart_message(cart, now):
    if not cart:
        return None
    n = len(paperbacks(cart))
    free = free_books(cart, now)
    if free:
        names = " and ".join(b["title"] for b in free)
        return (f"Bundle & Save: {names} free. You save ${saving(cart, now):.2f}. "
                f"Offer ends 30 November, 23:59:59.")
    if offer_is_on(now) and n % 3 == 2:
        return "Add 1 more paperback and the cheapest one is free."
    return None


def find_books(query):
    q = query.strip().lower()
    return [b for b in BOOKS if q and q in b["title"].lower()] if q else []


def filter_by_format(fmt):
    return [b for b in BOOKS if b["format"] == fmt]


def show_badge():
    return CAMPAIGN_ACTIVE


def price_text(book):
    return f"${book['price']:.2f}"


def book_page(title):
    for b in BOOKS:
        if b["title"] == title:
            return {"status": 200, "title": b["title"], "price": price_text(b)}
    return {"status": 404}


def login(user, password):
    u = USERS.get(user)
    if u and u["password"] == password:
        return {"ok": True, "orders": list(u["orders"])}
    return {"ok": False, "orders": []}


def order_history(user):
    return sorted(USERS[user]["orders"], reverse=True)


def logout(session):
    session.clear()
    return session


def wishlist_add(wishlist, title):
    return wishlist if title in wishlist else wishlist + [title]


def wishlist_remove(wishlist, title):
    return [t for t in wishlist if t != title]
