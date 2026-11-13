# Reading Group Notes assistant · its guards

**Practice data only.** The practice online bookshop is separate from Harbourleaf. Every name, date and note in these files is made up for teaching. Never paste real or work data into an AI assistant.

## The job

The Reading Group Notes assistant turns meeting notes into follow-ups and posts a summary to the group page. Meera, the AI Evaluation Engineer, has asked you to check the **guards** around it: the code that decides what the assistant may read and what it may post. A guard is code, not an instruction in the prompt.

No model is called. The guards are small pieces of plain Python, and each returns a `GuardResult`: a decision (ALLOW, BLOCK or ESCALATE), a reason for the log, and the message a member sees.

## The policy: what each decision means

| Decision | When | What the member sees |
|---|---|---|
| ESCALATE | A note reports a safety concern or an injury at a meeting | A message saying a person has been told and will follow up |
| BLOCK | A note asks for a member's phone number, email or home address to go in the summary | A message saying what was not done and why |
| ALLOW | Everything else | The normal summary |

An **over-block** is a harmless note that a guard stops or sends to a person.

## The output guard

The output guard checks the summary before it is posted. It looks for a phone number or an email address. A summary that has either must not be posted.

## The confidence floor (step 4)

Each summary gets a similarity score (how closely it matches the group's own notes). A summary scoring **below the floor** goes to a person. A labelled set of 200 summaries is supplied: 40 unsafe and 160 safe, and the mix mirrors traffic. The group posts **3,000 summaries a month**. The team can review **1,100 a month**. The compliance bar is **recall 0.90** on unsafe summaries. Choosing the floor is a decision: say who chose it.

## Words used in this Task

| Term | Meaning here |
|---|---|
| Precision | Of everything a guard stopped, the share that should have been stopped |
| Recall | Of everything that should have been stopped, the share the guard stopped |
| Over-block rate | Harmless cases stopped or sent to a person, out of all harmless cases |
| Fail-safe | When a guard cannot run, the system holds the reply back or hands it to a person |
| Fail-open | When a guard cannot run, the system lets the reply through |
| Reporting rule | Below 30 cases, report a count such as "k of N". Report a rate as a number only from 30 cases |

## Folder map

| File | What it is |
|---|---|
| `notes_brief.md` | This note: start here |
| `answers_notes.md` | Your reasons, step by step |
| `snippets.json`, `input_guard.py`, `test_decision_table.py` | Step 2: eight snippets, the input guard, and your decision table |
| `planted.json`, `output_guard.py`, `test_output_guard.py` | Step 3: planted values, the output guard, and your two tests |
| `scores.csv`, `threshold.py`, `test_threshold.py` | Step 4: the scores and the table (one function to write) |
| `guarded_call.py`, `test_failsafe.py` | Step 5: the guard runner with three faults, and your fail-safe test |
| `harmless.json`, `refusal_count.py` | Step 6: twenty harmless snippets and the refusal list |
| `track_scenarios.json`, `run_gate.py`, `test_tracks.py` | Step 7: your track |

Run `python -m pytest -q` from this folder.
