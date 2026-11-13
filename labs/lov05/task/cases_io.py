"""Loads and checks cases.json. Supplied: read it, do not change it."""
import json
from pathlib import Path

from probe_agent import CLASSES, SURFACES

FIELDS = {"id", "surface", "payload_class", "safe_behaviour"}


def load_cases():
    path = Path(__file__).parent / "cases.json"
    return json.loads(path.read_text(encoding="utf-8"))["cases"]


def problems(cases):
    """A list of what is wrong with the case file. An empty list means it is well formed."""
    found = []
    if len(cases) < 6:
        found.append("need at least 6 cases, found %d" % len(cases))
    seen = set()
    per_surface = {}
    for c in cases:
        if set(c) != FIELDS:
            found.append("%s: fields must be exactly %s" % (c.get("id", "?"), sorted(FIELDS)))
            continue
        if c["id"] in seen:
            found.append("duplicate id " + c["id"])
        seen.add(c["id"])
        if c["surface"] not in SURFACES:
            found.append("%s: surface must be one of %s" % (c["id"], list(SURFACES)))
        if c["payload_class"] not in CLASSES:
            found.append("%s: payload_class must be a class tag from payload_classes.md, nothing else" % c["id"])
        if not 10 <= len(c["safe_behaviour"]) <= 200 or "<<" in c["safe_behaviour"]:
            found.append("%s: safe_behaviour must be 10 to 200 characters of plain description, with no tag in it" % c["id"])
        per_surface.setdefault(c["surface"], set()).add(c["payload_class"])
    if not any(c.get("payload_class") == "<<tries:add_followup_chosen>>" for c in cases):
        found.append("at least one case must use the class <<tries:add_followup_chosen>> (Step 5 tests it)")
    if len(per_surface) < 3:
        found.append("cases must cover at least 3 surfaces, found %d" % len(per_surface))
    for s, classes in per_surface.items():
        if len(classes) < 2:
            found.append("surface %s needs at least 2 different classes" % s)
    return found
