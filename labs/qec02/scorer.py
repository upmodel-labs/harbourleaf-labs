"""Lab scorer for qec02 (practice files only, standard library only).

    python scorer.py fitness <set.csv> [--traffic <file>] [--baseline <file>] [--stale-before YYYY-MM-DD]
    python scorer.py agree <double.csv> [--bar 90]
    python scorer.py compare --baseline <b.json> --runs <r1.json> <r2.json> <r3.json>
    python scorer.py baseline --runs <r1.json> <r2.json> <r3.json> --tolerance <T> --out <file>

Set files (CSV) have the columns: id, slice, text, label, label_date, set_version.
Double-labelled files have: id, text, label_a, label_b.
Traffic files have: slice, share (percent of recent traffic).
Baseline and run files are JSON: score, prompt, model, set (a baseline also has tolerance).
"""
import argparse
import csv
import json
import sys
from collections import Counter, OrderedDict

MIN_TO_GATE = 10      # a slice under 10 cannot gate
MIN_FOR_RATE = 30     # from 30 a rate can be quoted; under 30, report a count
RUNS_MIN, RUNS_MAX = 3, 5


class Stop(Exception):
    """The scorer refuses to go on; the message says why."""


def read_csv(path):
    try:
        with open(path, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except OSError as e:
        raise Stop(f"cannot read {path}: {e.strerror}")


def read_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except OSError as e:
        raise Stop(f"cannot read {path}: {e.strerror}")
    except ValueError as e:
        raise Stop(f"{path} is not valid JSON: {e}")


def need(rows, columns, path):
    if not rows:
        raise Stop(f"{path} has no rows")
    missing = [c for c in columns if c not in rows[0]]
    if missing:
        raise Stop(f"{path} is missing the column(s): {', '.join(missing)}")


def num(x):
    """Format a score: 2 decimals when exact, otherwise up to 4."""
    s = f"{x:.4f}".rstrip("0")
    whole, _, frac = s.partition(".")
    return f"{whole}.{frac.ljust(2, '0')}"


def pct(n, total):
    return f"{round(100 * n / total)}%"


# ---------------------------------------------------------------- fitness
def unique_rows(rows):
    seen, out = set(), []
    for r in rows:
        key = (r["slice"], r["text"])
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out


def cmd_fitness(a):
    rows = read_csv(a.set)
    need(rows, ["slice", "text", "label_date", "set_version"], a.set)
    uniq = unique_rows(rows)
    dup = len(rows) - len(uniq)
    out = []

    out.append(("duplicates", "FLAG" if dup else "OK",
                f"{dup} duplicate rows ({len(uniq)} unique of {len(rows)})" if dup else f"no duplicate rows ({len(rows)} rows)"))

    sizes = OrderedDict()
    for r in uniq:
        sizes[r["slice"]] = sizes.get(r["slice"], 0) + 1
    small = [(s, n) for s, n in sizes.items() if n < MIN_TO_GATE]
    if small:
        bits = "; ".join(f"{s} has {n}, under {MIN_TO_GATE}, so it cannot gate" for s, n in small)
        rate = [f"{s} {n}" for s, n in sizes.items() if n >= MIN_FOR_RATE]
        count = [f"{s} {n}" for s, n in sizes.items() if MIN_TO_GATE <= n < MIN_FOR_RATE]
        if rate:
            bits += "; a rate can be quoted for " + ", ".join(rate)
        if count:
            bits += "; count only for " + ", ".join(count)
        out.append(("slice sizes", "FLAG", bits))
    else:
        low = min(sizes.values())
        tail = "none at 30, so counts only" if max(sizes.values()) < MIN_FOR_RATE else "slices from 30 can quote a rate"
        out.append(("slice sizes", "OK", f"smallest {low}; {tail}"))

    if a.baseline:
        base = read_json(a.baseline)
        versions = sorted({r["set_version"] for r in rows})
        want = base.get("set")
        if versions == [want]:
            out.append(("set version", "OK", f"set {want} = baseline set {want}"))
        else:
            out.append(("set version", "FLAG", f"set is {'/'.join(versions)}, the baseline was taken on set {want}"))
    else:
        out.append(("set version", "SKIPPED", "no --baseline given"))

    if a.stale_before:
        old = [r for r in rows if r["label_date"] < a.stale_before]
        out.append(("stale labels", "FLAG" if old else "OK",
                    f"{len(old)} labels written before {a.stale_before}" if old else f"0 labels written before {a.stale_before}"))
    else:
        out.append(("stale labels", "SKIPPED", "no --stale-before given"))

    if a.traffic:
        traffic = read_csv(a.traffic)
        need(traffic, ["slice", "share"], a.traffic)
        flags = []
        for t in traffic:
            share_traffic = float(t["share"])
            share_set = 100 * sizes.get(t["slice"], 0) / len(uniq)
            if share_set < share_traffic / 2:
                flags.append(f"{t['slice']} are {round(share_set)}% of the set, {round(share_traffic)}% of recent traffic")
        out.append(("coverage", "FLAG" if flags else "OK",
                    "; ".join(flags) if flags else "every slice has at least half its share of recent traffic"))
    else:
        out.append(("coverage", "SKIPPED", "no --traffic given"))

    for name, status, text in out:
        print(f"{name + ':':<14}{status:<8}{text}")
    return 0


# ------------------------------------------------------------------ agree
def cmd_agree(a):
    rows = read_csv(a.double)
    need(rows, ["label_a", "label_b"], a.double)
    agree = sum(1 for r in rows if r["label_a"].strip() == r["label_b"].strip())
    p = round(100 * agree / len(rows))
    verdict = "PASS" if p >= a.bar else "FAIL"
    print(f"{agree} of {len(rows)} agree = {p}%, bar {a.bar:g}%: {verdict}")
    return 0


# ------------------------------------------------- compare / baseline
def load_runs(paths):
    if not (RUNS_MIN <= len(paths) <= RUNS_MAX):
        raise Stop(f"give {RUNS_MIN} to {RUNS_MAX} runs, not {len(paths)}: one run is not a result")
    runs = [read_json(p) for p in paths]
    for p, r in zip(paths, runs):
        for k in ("score", "prompt", "model", "set"):
            if k not in r:
                raise Stop(f"{p} has no '{k}'")
    for k in ("prompt", "model", "set"):
        if len({r[k] for r in runs}) != 1:
            raise Stop(f"the runs do not share one {k}: {sorted({r[k] for r in runs})}")
    return runs


def mean(runs):
    return sum(float(r["score"]) for r in runs) / len(runs)


def cmd_compare(a):
    base = read_json(a.baseline)
    for k in ("score", "tolerance", "prompt", "model", "set"):
        if k not in base:
            raise Stop(f"{a.baseline} has no '{k}'")
    runs = load_runs(a.runs)
    if runs[0]["set"] != base["set"]:
        raise Stop(f"baseline was taken on set {base['set']}, the runs are on set {runs[0]['set']}; take a new baseline first")
    if runs[0]["model"] != base["model"]:
        raise Stop(f"baseline was taken on model {base['model']}, the runs are on model {runs[0]['model']}; take a new baseline first")
    m = mean(runs)
    line = float(base["score"]) - float(base["tolerance"])
    ok = round(m, 6) >= round(line, 6)
    scores = " · ".join(num(float(r["score"])) for r in runs)
    print(f"baseline {num(float(base['score']))} (prompt {base['prompt']}, model {base['model']}, set {base['set']}), tolerance {num(float(base['tolerance']))}")
    print(f"runs of prompt {runs[0]['prompt']}: {scores}")
    print(f"mean {num(m)}, line {num(line)}: {'PASS' if ok else 'WORSE'}")
    return 0


def cmd_baseline(a):
    runs = load_runs(a.runs)
    m = mean(runs)
    rec = {"score": round(m, 4), "tolerance": a.tolerance, "prompt": runs[0]["prompt"],
           "model": runs[0]["model"], "set": runs[0]["set"], "runs": [float(r["score"]) for r in runs]}
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=1)
        f.write("\n")
    scores = " · ".join(num(float(r["score"])) for r in runs)
    print(f"baseline {num(m)} ({scores}), line {num(m - a.tolerance)}")
    print(f"recorded: prompt {rec['prompt']}, model {rec['model']}, set {rec['set']} -> {a.out}")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="scorer.py", description="qec02 lab scorer (practice files only)")
    sub = p.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("fitness", help="can this scored set be trusted to gate?")
    f.add_argument("set")
    f.add_argument("--traffic")
    f.add_argument("--baseline")
    f.add_argument("--stale-before", dest="stale_before", metavar="YYYY-MM-DD")
    f.set_defaults(fn=cmd_fitness)

    g = sub.add_parser("agree", help="label agreement on a double-labelled sample")
    g.add_argument("double")
    g.add_argument("--bar", type=float, default=90)
    g.set_defaults(fn=cmd_agree)

    c = sub.add_parser("compare", help="mean of the runs against baseline minus tolerance")
    c.add_argument("--baseline", required=True)
    c.add_argument("--runs", nargs="+", required=True)
    c.set_defaults(fn=cmd_compare)

    b = sub.add_parser("baseline", help="take the mean of the runs as a new baseline")
    b.add_argument("--runs", nargs="+", required=True)
    b.add_argument("--tolerance", type=float, required=True)
    b.add_argument("--out", required=True)
    b.set_defaults(fn=cmd_baseline)

    a = p.parse_args(argv)
    try:
        return a.fn(a)
    except Stop as e:
        print(f"STOP: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
