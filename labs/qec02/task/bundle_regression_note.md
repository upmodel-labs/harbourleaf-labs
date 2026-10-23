# Bundle & Save: the change and the suite

*From Priya, QA Lead. The practice bookshop. All data here is fictional.*

## The change

The Bundle & Save offer's end time moves from **23:59:59** to **20:00:00** store time on **30 November**. The change was decided on **14 October**.

Bundle & Save: with 3 paperbacks in the cart, the cheapest is free; with 6, the two cheapest. Hardbacks never count.

## What reads the end time

`dependencies.csv` lists which areas of the site read the offer's end time. It is the evidence for what the change touches. The catalogue badge reads a separate `campaign_active` flag, which the same job sets, so it does not read the clock.

## The suite

- Full nightly run, by area: `areas.csv` (six areas, tests and minutes). This is last night's run.
- The 30 runnable tests in `tests/` are a small practice copy of the suite. Run them with `pytest` from this folder.
- `nightly_runs.csv` and `builds.csv`: the last 10 nightly runs of 8 of the tests, and what changed in each build.
- The scored set for the cart message, `offer_messages_set.csv`, was labelled by the team: each message is marked right or wrong for whether it states the right saving and the right end time. `baseline.json` is the last accepted score and `run_1.json` to `run_3.json` are three runs of the new message prompt.

## Your task

Follow the steps in Task HLF-P52 in UpModel. Keep your answers in a notes file or a spreadsheet.
