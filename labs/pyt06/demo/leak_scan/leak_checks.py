# leak_checks.py - Brian's leak checks for the order-help assistant
KNOWN_ORDERS = ["48213", "51007", "52114"]


def is_reply_safe(reply, own_order, known_orders=KNOWN_ORDERS):
    """True if the reply names no order except the customer's own."""
    for order in known_orders:
        if order != own_order and order in reply:
            return False
    return True
