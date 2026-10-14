# sdt02 · DDL, DML & Test Data Management

Practice files for the chapter's screen recording and for Task **HLF-P42 "Bookshop test data kit"**.
All data is fictional. Every `.sql` file drops and rebuilds its own schemas, so you can run it again at any time.

| File | What it builds |
|---|---|
| `demo/harbourleaf_testdata.sql` | Harbourleaf practice data used in the video: schema `hl_data` |
| `task/bookshop_testdata.sql` | The practice online bookshop (separate from Harbourleaf): schemas `bookshop_a` and `bookshop_b`, two branches with the same tables |

**Your own work goes in a schema of your own, `p42`.** Your teardown removes `p42` and, on the test-runs track, only the test orders you marked as yours.
If you reload `bookshop_testdata.sql` after building `p42`, run your teardown and then `setup.sql` again: reloading removes `p42`'s link to `bookshop_a.books`.

## Route 1 · pgAdmin
Open the `labs` database → Tools → Query Tool → open `task/bookshop_testdata.sql` → run it (F5).

## Route 2 · GitHub Codespaces
Use the configuration **"SQL & Database Testing (PostgreSQL)"**, then in the terminal:
```
psql -d labs -f labs/sdt02/task/bookshop_testdata.sql
psql -d labs -f setup.sql
psql -d labs -f teardown.sql
```

## Change data like a tester
1. Preview with a `SELECT` and the same `WHERE`; write down the count you expect.
2. `BEGIN;` → make the change → compare the count PostgreSQL reports.
3. `COMMIT;` if it matches, `ROLLBACK;` if it doesn't.
