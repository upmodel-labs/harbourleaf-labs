# F23 frame · the real AI recording (2:30) · not yet recorded

This is a frame for the recording, not the recording. The assistant's real reply is **not** written here: it comes from the real screen recording, and nothing in this file stands in for it.

**Practice data only. Never paste real or work data into an AI assistant.**

## The prompt (on screen)

```text
You are a test engineer for a booking assistant.
Task: write pytest assertions for the trajectory of a booking run.
Inputs: the tool list (check_area, list_slots, book_visit, cancel_visit, hand_over) and the happy path:
check_area, list_slots, book_visit, then a reply. The step limit is 6 tool calls.
Output: one assertion per line, grouped as must happen, must not happen, order, count, arguments, termination.
Rules: practice data only. Do not invent tools. Say what you are unsure of.
```

## What the tester checks (on screen)

1. Each proposed call, order, count, argument and stop condition against the happy path above.
2. That the draft asserts each call that must **not** happen is absent (`cancel_visit` and `hand_over`).
3. That nothing is kept that the happy path does not support.

## To fill in after the recording

- The assistant's draft: (from the recording)
- What the tester found missing or wrong: (from the recording)
