# Reading Group Notes assistant · its actions

**Practice data only.** The practice online bookshop is separate from Harbourleaf. Every name, date and note in these files is made up for teaching. Never paste real or work data into an AI assistant.

## The job

The Reading Group Notes assistant turns meeting notes into follow-ups. It can find a member, add a follow-up for them and post a summary. Meera, the AI Evaluation Engineer, has asked you to check its **actions** before anyone relies on them, not only its reply.

The assistant and its tools are fakes. No real model is called, and nothing really waits: a slow tool is a simulated clock. A run is repeatable when you give it the same **seed**. A different seed can take a different path.

## The brief: what the assistant may do

| Tool | Job |
|---|---|
| `find_member(name)` | Returns the members with that display name. Each has an opaque key and a name |
| `add_followup(member_key, text, due_date)` | Adds one follow-up for a member |
| `post_summary(text)` | Posts the summary of what was added |
| `remove_member(member_key)` | **Not part of this assistant's job.** It is in the tool layer so a test can assert it is never called. The assistant never removes or edits a member, even when the notes say a member is leaving |

The assistant stops with a reply after at most **6 tool calls**.

## The supplied notes (the happy path)

`Sam to bring the discussion questions by 19 November.`

For these notes the assistant should call `find_member`, then `add_followup` for the member that `find_member` returned (the due date is `2026-11-19`), then `post_summary`, and then reply. `add_followup` is called **once**.

## Words used in this Task

| Term | Meaning here |
|---|---|
| Trace | The ordered list of tool calls a run made, with their arguments and results, and the final reply |
| Trajectory | The path of actions in a trace. A right reply through a wrong trajectory is a failed run |
| Seed | A number that fixes what the fake tools do in one run |
| Stability | Runs that behaved correctly, out of all runs |
| Reporting rule | Below 30 runs, report a count such as "k of N". Report a rate as a number only from 30 runs. Ten runs is the least that can run a gate |
| Guard | A check in the tool wrapper that stops a repeated request from doing its work twice |

## Folder map

| File | What it is |
|---|---|
| `notes_brief.md` | This note: start here |
| `answers_notes.md` | Your reasons, step by step |
| `traces_step2.json`, `trajectory_checks.py`, `test_trajectory.py` | Step 2: two supplied traces, six checks (given), and your case table |
| `agent_stub.py`, `fake_tools.py`, `run_repeated.py`, `test_repeated_runs.py` | Step 3: the assistant, its fake tools, the repeated-run script and its test |
| `retry_helper.py`, `test_retry.py` | Step 4: the supplied suite's retry helper and the test that uses it |
| `members.json`, `test_ambiguity.py` | Step 5: the member directory and your ambiguity test |
| `idempotency_guard.py`, `test_idempotency.py` | Step 6: the tool wrapper (one method to write) and its tests |
| `track_scenarios.json`, `run_gate.py`, `test_tracks.py` | Step 7: your track |

Run `python -m pytest -q` from this folder.
