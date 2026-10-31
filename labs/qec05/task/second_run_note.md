# Bundle & Save, second run: the note

Practice data. This is the practice online bookshop. It is separate from Harbourleaf, and everyone in this note is fictional.

## From Priya, the QA (quality assurance) Lead, Monday 08:15

"I'm on the Room Match launch calls all week, so you lead the testing of the bookshop's Bundle & Save second run. A new tester joins us today. I asked them to explore the test bookshop for an hour this morning and send what they found. It is in `new_tester_defect_reports.md`. Plan the week, share out the work, help the new tester, keep the bookshop's product owner informed, and agree with the developer how fixes come back to us."

## The facts

- **The offer.** Bundle & Save gives a saving when a customer buys the books of one bundle (a set of books sold together). The basket shows a saving line, and a short cart message under the basket says what was saved and when the offer ends. A model writes the cart message.
- **The first run** ended at 20:00 store time on 30 November. On its last evening the saving kept being given after the end time. The developer put a fix into the QA environment last Friday.
- **The second run** opens on **Thursday at 09:00 store time**. Thursday is release day: no test work is planned on Thursday.
- **Work days:** Monday, Tuesday and Wednesday.
- **Who is who.**
  - You lead the test work.
  - **Harry** (AI Test Automation Engineer) looks after the pipeline.
  - **Meera** (AI Evaluation Engineer) looks after the model answers and the scored set.
  - **Brian** (AI Red Teamer, in Toronto) looks after the attack logs and the probe sessions.
  - **A new tester** starts today.
  - **The developer** fixes defects and says what a fix takes.
  - **The bookshop's product owner** decides whether the second run opens, and accepts any risk or anything left out.
- **The QA (quality assurance) environment.** There is one. Only one person can test on it at a time.
  - Monday and Wednesday it is free all day (10 hours each day).
  - **Tuesday it is free for testing for only 6 hours** (08:00 to 14:00). The developer deploys after 14:00.
- **Free hours.** `team.csv` gives the hours each person can give to this run, after their Room Match launch work and other jobs. Plan inside them.
- **The work.** `work_items.csv` lists 8 items. `risk_order` 1 is the highest risk, 8 the lowest. The risk order is already agreed: do not re-score it. Each item is one block of hours: one owner, one day.
- **Items marked "experienced tester"** are not for the new tester to do alone. Items marked "anyone" are.
- **The probe sessions.** Brian's probe sessions try to change the cart message through the book description of a test book in the QA environment. Brian wants to run the first one on Tuesday, his first day (item W05). The new tester joins it, on the day it runs, and it uses 2 of their free hours that day.
- **The label rule for a cart message.** A cart message is **right** if it states the saving that is in the basket, states the end time 20:00, and adds nothing the offer does not say. When no saving applies, the right message says so. Otherwise it is **wrong**.

## The new tester's first work

`new_tester_defect_reports.md` holds two defect reports. The developer reads defect reports to repeat each fault. Call the author "the new tester".

---

## Tuesday 17:00 update (open this part at step 5)

It is now Tuesday, 17:00. `results_tuesday.csv` shows where every item stands. Your plan from step 2 may have put some items on other days; for the status note, use these results.

What changed since Monday:

1. **The end-time re-test did not pass.** See item W01 in `results_tuesday.csv`. The pull-request regression run on Tuesday fails on a test for the same thing.
2. **The load-test finding from chapter 4:** put the finding you filed at the end of chapter 4 in your note as one line: where p95 (the 95th percentile: 95 in every 100 replies were that fast or faster) first went over the threshold, and whether that is above or below the expected peak. If you do not have it, write the line as an open item: "Load test: not done yet, so the risk at the expected peak is open."
3. **The developer says** he can switch the offer off by hand at 20:00 on Thursday if the product owner asks. He needs to know by Wednesday 16:00 (see `messages.md`).
