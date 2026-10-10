# HLF-P33 · Count what's in the file

**From:** Priya, QA Lead · **About:** 60 min · **Chapter:** Python for Testers · Lists, Tuples, Dictionaries & JSON Test Data
**Not scored. Unlimited attempts.**

> **The bookshop** is the practice online bookshop that Priya's Tasks use. It is separate from Harbourleaf, the store in the videos, and all of its data is fictional.

> "The practice bookshop has sent its catalogue as JSON and as CSV. Before anyone tests against it, I need to know what's in it: how many books, which categories, and whether anything is listed twice."

## Files in this folder

| File | What it holds |
|---|---|
| `bookshop_catalogue_v1.json` | The catalogue: id, title, category, price, isbn, stock, in_stock |
| `bookshop_catalogue_v1.csv` | The same catalogue, exported as CSV |
| `bookshop_run.csv` | Track *Test runs*: check_id, status, seconds |
| `book_answers.jsonl` | Track *Model answers*: question, answer, expected (one JSON object per line) |
| `bookshop_attacks.jsonl` | Track *Attack logs*: id, language (`en` English, `cy` Welsh), payload, got_through |
| `demo/` | The files used in the chapter's demo, if you want to follow along |

Put your script in this folder so the file names work as they are. In Colab, upload the files first (the folder icon on the left).

## Steps

### 1. Get the files (5 min)
On the repo's main page, choose **Code → Download ZIP**, then unzip it. Open the `labs/pyt03` folder in VS Code, or upload its files to Colab.

### 2. Load and count (9 min)
Load `bookshop_catalogue_v1.json`. Print how many rows it has and how many rows are in each category (use a dictionary).

### 3. Listed twice? (10 min)
Find any `id` that appears more than once. Print the duplicates and the number of unique ids.

### 4. Same data, as CSV (12 min)
For the first row, print each field's type in the JSON file and in the CSV file (read the CSV with `csv.DictReader`). Then say which values would give a wrong answer in an `if` or a sort.

### 5. Write the summary (10 min)
Write `summary.json` with the number of rows, the number of unique ids, the count per category and the duplicates (`json.dump` with `indent=2`).

### 6. Your track (10 min)

| Track | Task |
|---|---|
| Test runs | From `bookshop_run.csv`, list the failed checks and the 3 slowest. Convert the seconds first. |
| Model answers | In `book_answers.jsonl`, count exact matches, then matches after `strip()` and `lower()`. List what is still wrong. |
| Attack logs | In `bookshop_attacks.jsonl`, count attacks and successes per language, and list the ids that got through. |

### 7. Paste your evidence (4 min)
Paste your code, its output and `summary.json` into the Task panel in UpModel.

## Hints
- `with open("file.json", encoding="utf-8") as f:` then `json.load(f)` for one JSON document.
- JSON Lines: loop over the file and use `json.loads(line)` for each line.
- CSV: `open(..., newline="")`, then `list(csv.DictReader(f))`. **Every CSV value is text.**
- Count with a dictionary: `counts[key] = counts.get(key, 0) + 1`.
