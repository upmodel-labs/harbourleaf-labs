# HLF-P54 · Bundle & Save second run · load-test note

From: Priya, QA Lead

This is the practice online bookshop and its Bundle & Save offer. It is separate from Harbourleaf. The first run has finished. Before the second run opens, we need to know whether the basket and checkout hold when most shoppers arrive in the first minutes.

## The facts you need

- **Second run opens:** Thursday 10 December at 09:00 store time.
- **The crowd to plan for:** the same shoppers, at the same times, as the first run. Their arrivals are in `first_run_traffic.csv`: one row for each of the first 30 minutes after opening.
- **How long a visit lasts:** about 3 minutes (from the first run's logs).
- **Think time:** a shopper pauses 10 to 14 seconds between pages.
- **The three journeys:** browse (look at the books), basket (add the Bundle & Save offer to the basket), checkout (pay). The columns of `first_run_traffic.csv` count shoppers by the furthest step they reached.
- **The request mix for this lab:** use each journey's share of shoppers as the mix of requests. This is a simplification: a shopper who pays has also browsed and added to the basket, but we do not count those extra requests. A Locust task weight sets how often a request is picked, so say in your model that you simplified.

## The threshold

THRESHOLD AT THE EXPECTED PEAK: p95 response time at most 2500 milliseconds (ms), which is 2.5 seconds, and error rate at most 1% of requests.

The threshold names the percentile, the load and the error rate. It is the exit criterion for this test, as in chapter 1.

**Reading the stages against the expected peak.** No stage of the run is at exactly the expected peak, so reason from the stages either side of it:

- If a stage below the peak is already over the threshold, the service does not meet the threshold at the peak: response time rises with users.
- If a stage at or above the peak passes, the peak is met. The headroom you have proved is only the gap up to the highest stage that passed, not up to the next stage.
- If the highest passing stage is below the peak and the first failing stage is above it, the run cannot say. Report that, and recommend a stage at the peak.

## How the practice service works (use these as your facts)

- It has **one worker**: it handles one request at a time. Other requests wait in a queue.
- A request that waits more than **4 seconds** gets a 503 reply ("busy"). The 503 comes back after about 4000 ms.
- It holds no data and is connected to nothing. The cart message on the basket reply is a plain template; in the story a model writes it.
- Only ever load-test this service, started by you. Never point a load test at a site you do not own or have written permission to test.

## How the results file is counted

`stepped_run.csv` is a simulated reference run of this service in five stages of rising users. It is a simulation of the same one-worker service, built for teaching. It is not a recording of a real system, and it is practice data made for this lab.

- Each stage was measured for **30 seconds**, after the users had settled. Each row is one request that finished in those 30 seconds.
- **Count every row of a stage**, including the 503 rows, for the percentiles. A shopper who waits 4 seconds and then sees "busy" has had a slow reply.
- **Error rate** = rows with status 503 divided by all rows of the stage.
- Use the spreadsheet function `PERCENTILE.INC` for p95 (the 95th percentile, `0.95`).
- Only if you want more: p50 uses `0.5`, and requests per second = all rows of the stage divided by 30.

## Where the results go

A performance finding goes to triage like any defect (chapter 3). Write down the conditions and the date: these numbers belong to this service, this data and this day.
