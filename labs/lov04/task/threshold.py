"""Step 4: the threshold table.

An answer whose similarity score is BELOW the floor goes to a person (ESCALATE).
scores.csv: 200 labelled summaries, 40 unsafe and 160 safe. The mix mirrors traffic.

    python threshold.py          prints the score-against-correctness view, then the table

Write row(). Recall = unsafe answers sent to a person, out of all unsafe. Over-block = safe answers sent to a person,
out of all safe. escalated_share = answers sent to a person, out of all answers.
"""
import csv
from pathlib import Path

FLOORS = [0.50, 0.60, 0.70, 0.80]
MONTHLY_VOLUME = 3000        # answers a month
REVIEW_CAPACITY = 1100       # reviews a month the team can do
RECALL_BAR = 0.90            # the compliance bar on unsafe answers


def load_scores():
    with open(Path(__file__).parent / "scores.csv", encoding="utf-8") as f:
        return [(r["id"], float(r["score"]), int(r["unsafe"])) for r in csv.DictReader(f)]


def by_bin(scores, width=0.1):
    """Plain-Python binning: for each score band, how many answers are unsafe and how many are safe."""
    bins = {}
    for _, s, unsafe in scores:
        lo = round(int(s / width) * width, 2)
        b = bins.setdefault(lo, [0, 0])
        b[0 if unsafe else 1] += 1
    return dict(sorted(bins.items()))


def row(scores, floor):
    """Return (recall, over_block, escalated_share) for one floor. Write this."""
    raise NotImplementedError("Step 4: write row()")


def main():
    scores = load_scores()
    print("score band | unsafe | safe")
    for lo, (u, s) in by_bin(scores).items():
        print("%.1f-%.1f    | %6d | %4d" % (lo, lo + 0.1, u, s))
    print()
    print("floor | recall | over-block | reviews a month")
    for fl in FLOORS:
        recall, over, share = row(scores, fl)
        print("%.2f  | %.2f   | %.2f       | %d" % (fl, recall, over, round(share * MONTHLY_VOLUME)))


if __name__ == "__main__":
    main()
