"""When the low-stock label shows (Room Match demo, fictional)."""

LOW_STOCK_AT = 5          # the label shows at this many units or fewer


def low_stock_label(units_left):
    if 0 < units_left <= LOW_STOCK_AT:
        return f"Only {units_left} left"
    return ""
