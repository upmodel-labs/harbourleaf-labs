# Reading Group Notes assistant · probing it

**Practice data only.** The practice online bookshop is separate from Harbourleaf. Every name, date and note in these files is made up for teaching. Never paste real or work data into an AI assistant. **No attack text anywhere:** test material here is a payload class tag, nothing else.

## The job

Meera, the AI Evaluation Engineer, has asked you to probe the Reading Group Notes assistant before the group relies on it. Brian, the AI Red Teamer, will review your cases. The assistant turns meeting notes into follow-ups: it finds a member, adds a follow-up and posts a summary. It never removes a member, even though a `remove_member` tool exists in the tool layer so a test can assert it is never called.

The assistant is a fake. No model is called, nothing is sent anywhere, and the same run number always gives the same path.

## Your scope (written authority)

The practice bookshop's product owner has authorised you, in writing, to test **this practice assistant, in this lab only**. Nothing real is in scope: no live service, no real member, no real file.

## What we know about the four surfaces

| Surface | Facts |
|---|---|
| Pasted meeting notes | Pasted by the member who runs the meeting. Read once, for that meeting. The summary goes to the group page (five members) |
| A member's display name | Set by each member in their own profile. Read in every meeting's member lookup, every week, until the member changes it |
| The file name of an uploaded notes file | Chosen by whoever uploads the file. Read once, with that upload |
| The follow-up tool's error text | Written by the follow-up service. It can include parts of the request it received. Read once, in that run |

After reading, the assistant can call `find_member`, `add_followup` and `post_summary`. **Reach** is how many people or runs one planted text can affect.

## The policy for follow-ups (step 6)

At most **5** active follow-ups per member in one meeting. The tool must refuse the sixth and say why. This is a control in code, not a line in the assistant's instructions.

## Words used in this Task

| Term | Meaning here |
|---|---|
| Surface | A place outside text can reach the assistant from |
| Payload class | A kind of outside text, named by its effect and written as a tag |
| Trajectory | The calls the assistant made in one run, with their arguments |
| Reporting rule | Below 30 runs, report a count such as "k of N". Report a rate as a number only from 30 runs. A clean run is a claim about this version and these cases, not "safe" |
| Finding record | One line: surface, class, effect, k of N, assertion, status |
| Scope | What you are authorised to test, where, and what is out of bounds |

## Folder map

| File | What it is |
|---|---|
| `notes_brief.md`, `payload_classes.md` | This note and the class tags: start here |
| `answers_notes.md` | Your reasons, step by step |
| `inventory.md`, `test_inventory.py` | Step 2: the input inventory (yours) and its check |
| `cases.json`, `cases_io.py`, `test_cases_file.py` | Step 3: your class-based cases, and the check on the file |
| `probe_agent.py`, `effects.py`, `test_probe_runs.py` | Step 4: the fake assistant, the effect check, and your repeat-run test |
| `reply_check.py`, `test_trajectory.py` | Step 5: a reply-only check, and your trajectory test |
| `followup_tool.py`, `test_limit.py` | Step 6: the follow-up tool (write the limit) and your test |
| `run_regression.py` | Your track, T1: the regression file in one command |

Run `python -m pytest -q` from this folder.
