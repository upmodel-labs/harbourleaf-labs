"""Step 2: the inventory table must be complete, with four different priorities. The table is yours."""
from pathlib import Path


def _rows():
    lines = (Path(__file__).parent / "inventory.md").read_text(encoding="utf-8").splitlines()
    table = [l for l in lines if l.startswith("|")][2:]
    return [[c.strip() for c in l.strip("|").split("|")] for l in table]


def test_the_inventory_has_four_complete_rows():
    rows = _rows()
    assert len(rows) == 4
    for r in rows:
        assert all(r), "an empty cell in the row for: " + r[0]


def test_the_priorities_are_one_to_four_once_each():
    assert sorted(r[4] for r in _rows()) == ["1", "2", "3", "4"]
