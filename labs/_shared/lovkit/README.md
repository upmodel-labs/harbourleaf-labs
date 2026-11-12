# lovkit

The shared practice kit for the LLM and agent output validation labs. Standard library plus `pydantic`; no live model, no network.

| Name | What it is |
|---|---|
| `REFERENCE_DATE` | A fixed date (12 November 2026). Rules such as "not before the reference date" use it, never today's date |
| `MEMBERS` | The practice reading group's five members |
| `fake_notes_model(notes, flags=())` | A fake Reading Group Notes assistant: notes in, a JSON reply out. Defects are switched on by flags |
| `FakeBookingAssistant` and `make_requests()` | The booking assistant used in the demo recordings |
| `FakeGroundedAssistant(corpus, flags=(), served_version=...)` | A fake assistant that answers from a small corpus of numbered lines and says which line backs each claim. Flags switch defects on: `hallucinate`, `stale_note`, `drift`. Used with `load_corpus`, `line_ids`, `manifest_of` and `checksum` |

**Practice data only.** Every name, date and number is made up for teaching. Never paste real or work data into an AI assistant.
