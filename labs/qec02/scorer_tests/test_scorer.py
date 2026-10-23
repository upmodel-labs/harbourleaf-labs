import csv
import json
import re
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
TASK = LAB / "task"
DEMO = LAB / "demo" / "scorer"
sys.path.insert(0, str(LAB))

import scorer  # noqa: E402


def run(capsys, *argv):
    code = scorer.main([str(a) for a in argv])
    return code, capsys.readouterr().out


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ------------------------------------------------------------- Task
def test_task_fitness(capsys):
    code, out = run(capsys, "fitness", TASK / "offer_messages_set.csv", "--baseline", TASK / "baseline.json", "--stale-before", "2026-10-14")
    assert code == 0
    assert "FLAG" in out and "14 duplicate rows (106 unique of 120)" in out
    assert "mixed formats has 6" in out
    assert "set v1 = baseline set v1" in out
    assert "22 labels written before 2026-10-14" in out
    assert "SKIPPED" in out  # no traffic file


def test_task_agreement(capsys):
    _, out = run(capsys, "agree", TASK / "double_labelled.csv", "--bar", 90)
    assert "13 of 20 agree = 65%, bar 90%: FAIL" in out


def test_task_compare(capsys):
    _, out = run(capsys, "compare", "--baseline", TASK / "baseline.json", "--runs", TASK / "run_1.json", TASK / "run_2.json", TASK / "run_3.json")
    assert "mean 0.89, line 0.87: PASS" in out


def test_one_run_is_refused(capsys):
    code, out = run(capsys, "compare", "--baseline", TASK / "baseline.json", "--runs", TASK / "run_1.json")
    assert code == 2 and out.startswith("STOP:") and "one run is not a result" in out


def test_task_data_totals():
    areas = rows(TASK / "areas.csv")
    assert sum(int(a["tests"]) for a in areas) == 304
    assert sum(int(a["minutes"]) for a in areas) == 107
    data = rows(TASK / "offer_messages_set.csv")
    assert len(data) == 120
    assert len({(r["slice"], r["text"]) for r in data}) == 106
    deps = {r["read_by_area"] for r in rows(TASK / "dependencies.csv") if r["component"] == "offer_end_time"}
    assert deps == {"offer_rules", "cart_message", "checkout_total"}


def test_task_nightly_history():
    runs = rows(TASK / "nightly_runs.csv")
    flaky = sorted({int(r["run"]) for r in runs if r["test"] == "test_message_shown_with_saving" and r["result"] == "failed"})
    hard = sorted({int(r["run"]) for r in runs if r["test"] == "test_hardback_not_counted" and r["result"] == "failed"})
    assert flaky == [2, 5, 6, 9] and hard == [7, 8, 9, 10]
    assert all(r["rerun_result"] == "passed" for r in runs if r["test"] == "test_message_shown_with_saving" and r["result"] == "failed")
    assert all(r["rerun_result"] == "failed" for r in runs if r["test"] == "test_hardback_not_counted" and r["result"] == "failed")
    assert sum(1 for r in runs if r["result"] == "failed") == 8
    assert len(runs) == 80


def test_test_counts():
    def count(folder):
        return sum(len(re.findall(r"^def test_", p.read_text(), re.M)) for p in (folder / "tests").glob("test_*.py"))
    assert count(TASK) == 30
    assert count(LAB / "demo") == 40


# ------------------------------------------------------------- Demo
D = DEMO


def test_demo_fitness_before(capsys):
    _, out = run(capsys, "fitness", D / "set_d1.csv", "--traffic", D / "traffic_30d.csv", "--baseline", D / "baseline_d1.json", "--stale-before", "2026-10-08")
    assert "3 duplicate rows (60 unique of 63)" in out
    assert "smallest 11; none at 30, so counts only" in out
    assert "set d1 = baseline set d1" in out
    assert "0 labels written before 2026-10-08" in out
    assert "text descriptions are 18% of the set, 42% of recent traffic" in out


def test_demo_agreement(capsys):
    assert "14 of 20 agree = 70%, bar 90%: FAIL" in run(capsys, "agree", D / "double_labelled_d1.csv", "--bar", 90)[1]
    assert "20 of 20 agree = 100%, bar 90%: PASS" in run(capsys, "agree", D / "fresh_20_d2.csv", "--bar", 90)[1]


def test_demo_set_versions(capsys):
    d1, d2 = rows(D / "set_d1.csv"), rows(D / "set_d2.csv")
    assert len(d1) == 63 and len(d2) == 60
    assert {r["set_version"] for r in d1} == {"d1"} and {r["set_version"] for r in d2} == {"d2"}
    a = {r["id"]: r["label"] for r in d1}
    changed = [r["id"] for r in d2 if a[r["id"]] != r["label"]]
    assert len(changed) == 6


def test_demo_compare_stops_on_old_baseline(capsys):
    code, out = run(capsys, "compare", "--baseline", D / "baseline_d1.json", "--runs", *[D / f"runs_p6_d2_{i}.json" for i in (1, 2, 3)])
    assert code == 2
    assert out.strip() == "STOP: baseline was taken on set d1, the runs are on set d2; take a new baseline first"


def test_demo_new_baseline_then_worse(capsys, tmp_path):
    out_file = tmp_path / "baseline_d2.json"
    code, out = run(capsys, "baseline", "--runs", *[D / f"runs_p5_d2_{i}.json" for i in (1, 2, 3)], "--tolerance", 0.01, "--out", out_file)
    assert code == 0 and "baseline 0.54" in out and "line 0.53" in out
    rec = json.loads(out_file.read_text())
    assert (rec["prompt"], rec["model"], rec["set"]) == ("p5", "build", "d2")
    _, out = run(capsys, "compare", "--baseline", out_file, "--runs", *[D / f"runs_p6_d2_{i}.json" for i in (1, 2, 3)])
    assert "mean 0.49, line 0.53: WORSE" in out


# ------------------------------------------------------------- Copies
@pytest.mark.parametrize("copy", [TASK / "scorer.py", DEMO / "scorer.py"])
def test_scorer_copies_are_identical(copy):
    assert copy.read_text() == (LAB / "scorer.py").read_text()
