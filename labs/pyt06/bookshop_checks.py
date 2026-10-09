# bookshop_checks.py - the bookshop's shared checks (from Chapter 4)


def has_price(book):
    """True if the book has a price."""
    return book.get("price") is not None


def isbn_ok(book):
    """True if the ISBN is exactly 13 digits."""
    return len(book["isbn"]) == 13 and book["isbn"].isdigit()


def stock_ok(book):
    """True if stock is not negative."""
    return book["stock"] >= 0


def score_answer(answer, expected, case_sensitive=False):
    """True if the answer matches the expected answer (spaces at the ends ignored)."""
    if case_sensitive:
        return answer.strip() == expected.strip()
    return answer.strip().lower() == expected.strip().lower()


def payload_lower(attack):
    """The attack's payload in lower case, or "" if no payload was recorded."""
    if attack.get("payload") is None:
        return ""
    return attack["payload"].lower()
