"""A fake Reading Group Notes assistant: turns notes into a JSON reply, with no model.

Rules (the behaviour note in each lab explains them in plain words):
  * "<Name> to <do something> by <day> <Month>."  -> a task for a member
  * "Decision: ..."                                -> a decision, no owner
  * a line ending in "?"                           -> a question
  * a task for a name that is not a member         -> a question asking who that is
  * empty notes                                    -> no items
Flags switch defects on: "obey_tags" (a payload class tag changes the output),
"leak_phone" (a phone number appears in the summary).
"""
import json
import re

from .members import MEMBERS

_MONTHS = {m: i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July", "August",
     "September", "October", "November", "December"], start=1)}
_TASK = re.compile(r"^(?P<name>[A-Z][a-z]+) to (?P<what>.+?)(?: by (?P<day>\d{1,2}) (?P<month>[A-Za-z]+))?\.$")
_TAG = re.compile(r"<<tries:(?P<effect>[a-z_]+)>>")


def fake_notes_model(notes, flags=()):
    items = []
    for raw in (notes or "").splitlines():
        line = raw.strip()
        if not line:
            continue
        tag = _TAG.search(line)
        if tag:
            if "obey_tags" in flags and tag.group("effect") == "add_task_for_nonmember":
                items.append({"kind": "task", "owner": "Quinn", "text": "Follow up as instructed", "due": None})
            continue
        if line.startswith("Decision:"):
            items.append({"kind": "decision", "owner": None, "text": line[len("Decision:"):].strip(), "due": None})
        elif line.endswith("?"):
            items.append({"kind": "question", "owner": None, "text": line, "due": None})
        else:
            m = _TASK.match(line)
            if not m:
                continue
            if m.group("name") not in MEMBERS:
                items.append({"kind": "question", "owner": None, "text": "Who is " + m.group("name") + "?", "due": None})
                continue
            due = None
            if m.group("day"):
                due = "2026-%02d-%02d" % (_MONTHS[m.group("month")], int(m.group("day")))
            items.append({"kind": "task", "owner": m.group("name"), "text": m.group("what"), "due": due})
    summary = "%d action item%s from this meeting." % (len(items), "" if len(items) == 1 else "s") if items else "No action items were found."
    if "leak_phone" in flags:
        summary += " Questions: call 07700 900456."
    return json.dumps({"summary": summary, "items": items})
