"""A tiny Room Match for the demo (fictional): suggestions, cart, photo upload, account."""
from stock import low_stock_label

CATALOGUE = {
    "sofa-oak": {"name": "Oak sofa", "price": 499.0, "fit": 0.9},
    "rug-sand": {"name": "Sand rug", "price": 89.5, "fit": 0.8},
    "lamp-brass": {"name": "Brass lamp", "price": 45.0, "fit": 0.7},
    "shelf-pine": {"name": "Pine shelf", "price": 60.0, "fit": 0.6},
    "chair-grey": {"name": "Grey chair", "price": 120.0, "fit": 0.5},
    "table-white": {"name": "White table", "price": 150.0, "fit": 0.4},
}


def suggest(room_text, limit=5):
    if not room_text.strip():
        return []
    ranked = sorted(CATALOGUE.items(), key=lambda kv: -kv[1]["fit"])
    return [pid for pid, _ in ranked][:limit]


def suggestion_line(pid, units_left):
    item = CATALOGUE[pid]
    line = f"{item['name']}: it fits the style of your room."
    label = low_stock_label(units_left)
    return f"{line} {label}".strip()


def price_text(pid):
    return f"${CATALOGUE[pid]['price']:.2f}"


class Cart:
    def __init__(self):
        self.items = {}

    def add(self, pid, qty=1):
        if sum(self.items.values()) + qty > 10:
            raise ValueError("a cart holds at most 10 items")
        self.items[pid] = self.items.get(pid, 0) + qty

    def remove(self, pid):
        self.items.pop(pid, None)

    def set_qty(self, pid, qty):
        self.items[pid] = qty

    def total(self):
        return round(sum(CATALOGUE[p]["price"] * q for p, q in self.items.items()), 2)

    def line(self, pid, units_left):
        return suggestion_line(pid, units_left)

    def clear(self):
        self.items.clear()


ALLOWED = {".jpg", ".jpeg", ".png"}
MAX_BYTES = 5_000_000


def upload(name, size):
    ext = "." + name.rsplit(".", 1)[-1].lower() if "." in name else ""
    if size == 0:
        return {"ok": False, "reason": "empty file"}
    if ext not in ALLOWED:
        return {"ok": False, "reason": "unsupported type"}
    if size > MAX_BYTES:
        return {"ok": False, "reason": "too large"}
    return {"ok": True, "name": name}


ACCOUNTS = {"mira": "correct-horse-1"}


def sign_in(user, password):
    return ACCOUNTS.get(user) == password


def valid_password(pw):
    return len(pw) >= 10


class Account:
    def __init__(self, name):
        self.name = name
        self.rooms = []

    def save_room(self, room):
        self.rooms.append(room)

    def rename(self, name):
        self.name = name.strip()
