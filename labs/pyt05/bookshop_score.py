# bookshop_score.py - average review score for the bookshop's search answers
import json

GATE = 4.0          # the average must be at least 4.0
scores = []
passes = 0
total = 0
with open("search_scores.jsonl", encoding="utf-8") as f:
    for line in f:
        row = json.loads(line)
        score = int(row["score"])
        scores.append(score)
        if score >= 4:
            passes += 1
            total += score

average = total / len(scores)
print(f"answers scored: {len(scores)} · passes (4 or 5): {passes}")
if average >= GATE:
    print(f"average {average:.2f} · gate {GATE}: PASS")
else:
    print(f"average {average:.2f} · gate {GATE}: FAIL")
