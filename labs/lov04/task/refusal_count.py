"""Step 6: the refusal count on harmless notes.

    python refusal_count.py

Prints the input guard's decision for each of twenty harmless snippets. None of them should be stopped.
Count the ones that are, and write the result as k of 20 in answers_notes.md.
"""
import json
from pathlib import Path

from input_guard import check_input

SNIPPETS = json.loads((Path(__file__).parent / "harmless.json").read_text(encoding="utf-8"))["snippets"]


def main():
    for s in SNIPPETS:
        print("%s | %-8s | %s" % (s["id"], check_input(s["text"]).decision, s["text"]))


if __name__ == "__main__":
    main()
