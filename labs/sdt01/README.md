# sdt01 · SQL Queries & Joins for Testers

Practice files for the chapter's screen recording and for Task **HLF-P41 "Bookshop order checks"**.
All data is fictional. Every `.sql` file drops and rebuilds its own schema, so you can run it again at any time.

| File | What it builds |
|---|---|
| `demo/harbourleaf_orders.sql` | Harbourleaf practice data used in the video: schemas `harbourleaf`, `eval`, `redteam` |
| `task/bookshop_orders.sql` | The practice online bookshop (separate from Harbourleaf): schema `bookshop` |

## Get the files
On the repository page: Code → Download ZIP, then unzip it. (Codespaces users already have the files.)

## Route 1 · pgAdmin (on your computer)
1. Install PostgreSQL from postgresql.org (the Windows and macOS installers include pgAdmin).
2. In pgAdmin: Servers → your server → Databases → Create → Database, name it `labs`.
3. Select `labs` → Tools → Query Tool → open `task/bookshop_orders.sql` → run it (F5).
4. Run `SELECT version();` to check the connection.

## Route 2 · GitHub Codespaces (nothing to install)
1. On the repository page: Code → Codespaces → `...` → New with options → choose the configuration **"SQL & Database Testing (PostgreSQL)"** → Create.
2. In the terminal: `psql -d labs -f labs/sdt01/task/bookshop_orders.sql`
3. Then `psql -d labs` and type your queries (end each with `;`, quit with `\q`).

Linux users: take Route 2, unless you already run PostgreSQL and pgAdmin.

## Write it like a tester
Above each query, write the result you expect and what a non-empty result would mean:
```sql
-- expect 0 rows; any row is an order nobody can track
```
