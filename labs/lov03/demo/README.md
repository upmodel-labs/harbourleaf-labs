# Demo files · lab lov03 (Harbourleaf assembly booking)

The files behind the demo recording. The Task does not use them. Only three products appear: the Oakmere 4-shelf unit, the Halden 2-door wardrobe and the Tarn wall shelf.

| Box | Minutes | File | Used for |
|---|---|---|---|
| 1 | 1:30 | `test_visit_trajectory.py` (`test_a_slow_book_visit_makes_the_agent_book_again`) | A fake slow `book_visit`, swapped in with `monkeypatch`. The slowness is a simulated clock: nothing waits |
| 2 | 2:30 | `test_visit_trajectory.py` (the six assertions and the printed trace) | Tool called, tool not called, order, count, arguments, termination; the trace printed when one fails |
| 3 | 2:00 | `test_visit_trajectory.py`, `run_thirty.py` | The deliberate error: one run passes; `python run_thirty.py` runs 30 and counts |
| 4 | 1:00 | `test_visit_trajectory.py` (`parametrize`) | One test over three products, and one case outside the service area |
| 5 | 1:30 | `visit_guard.py`, `python run_thirty.py --guard` | The guard in the tool wrapper, then the re-run |
| 6 | 2:30 | `f23_frame.md` | The script frame for the real AI recording (not yet recorded) |
| | | `visit_demo.py`, `_setup.py`, `conftest.py` | The assistant ready to run, and plumbing |

Run from this folder with `python -m pytest -q`. Practice data only.
