# Lab qec04 · Bundle & Save second-run load test (HLF-P54)

Practice files for the chapter "Performance & Load Testing" of the Quality Engineering Core module. You will plan the load for the practice online bookshop's second run, script it in Locust, run it against a small practice service, read a supplied results file, and write a finding.

Everything here is practice data made for the lab. There is no real shop, no real customer and no real data. The bookshop is separate from Harbourleaf.

**Only ever load-test the practice service in this lab, which you start yourself. Never point a load test at a site you do not own or have written permission to test.**

## What is in the folder

| File | What it is |
|---|---|
| `bundle_loadtest_note.md` | Start here. Priya's note: the facts, the second-run opening time, the threshold, how to read the stages against the expected peak, and how the results file is counted |
| `first_run_traffic.csv` | Shoppers arriving in each of the first 30 minutes of the first run, and which journey they followed |
| `bookshop_service.py` | The practice bookshop service. It has a known limit on purpose, so you can see response time bend |
| `locustfile.py` | The starter script. You finish it in step 3 |
| `stepped_shape.py` | A ready-made stepped load shape: five stages of rising users. You do not edit it |
| `stepped_run.csv` | A simulated reference run of the same one-worker service, about 300 rows, made for the lab (not a recording of a real system), for step 5 and the AI touch |
| `model_message_times.csv` | Response times of the cart message by basket size, for the Model answers track |
| `requirements.txt` | The tool to install (Locust, version pinned) |

## Set-up in GitHub Codespaces (free, in your browser)

1. Open the practice repo on GitHub (`harbourleaf-labs`), choose **Code**, then **Codespaces**, then **Create codespace on main**. Wait until the editor opens. This can take a minute or two.
2. Open a terminal in the editor (**Terminal**, then **New Terminal**) and run:

```bash
cd labs/qec04
pip install -r requirements.txt
python bookshop_service.py
```

The terminal now says the practice bookshop is running. Leave it running. To check it, open a second terminal and run `curl http://localhost:8080/health`: you should see `"status": "up"`. In Codespaces your own browser cannot reach `localhost:8080`; if you want to see the service in a browser, open port 8080 from the **Ports** tab.

3. In the second terminal, start Locust (this works once you have filled in the starter file in step 3):

```bash
cd labs/qec04
locust -f locustfile.py --host http://localhost:8080
```

4. Codespaces shows a message that port 8089 is available. Choose **Open in Browser**. If you miss it, open the **Ports** tab and open port 8089. That is the Locust page.
5. For the stepped run in step 4, stop Locust (Ctrl+C) and start it with the shape added:

```bash
locust -f locustfile.py,stepped_shape.py --host http://localhost:8080
```

The run takes 5 minutes, one minute for each of the five stages, and the user boxes on the page are ignored while the shape is active.

## Local fallback (your own computer)

You need Python 3.10 or newer. In a terminal, in this folder:

```bash
python -m venv venv
```

Activate it (on Windows `venv\Scripts\activate`, on Mac or Linux `source venv/bin/activate`), then run the same commands as above: `pip install -r requirements.txt`, then `python bookshop_service.py` in one terminal and the `locust` command in a second one (activate the venv there too). Open http://localhost:8089 for the Locust page.

## A few things worth knowing

- The service holds no data and is connected to nothing. It handles one request at a time, on purpose. The note explains what happens when requests queue.
- `python bookshop_service.py --no-saving` leaves the saving out of the basket reply. You use it in step 3 to prove that your response check catches the fault. Your check looks at the saving only on a normal (200) reply. A 503 "busy" reply is a different fault (the queue limit) and shows as its own error, not as a missing saving.
- `python bookshop_service.py --workers 2` lets it handle two requests at once. It is not part of the Task: it is there if you want to see what a fix does.
- If port 8080 is already in use, start the service with `--port 8081` and use `--host http://localhost:8081` in the Locust command.
- The numbers from your own stepped run depend on your machine. Steps 5 and 8 use the supplied `stepped_run.csv`, so everyone works from the same numbers.
- Locust documentation: https://docs.locust.io/en/stable/

## About the data

`first_run_traffic.csv`, `stepped_run.csv` and `model_message_times.csv` are synthetic: they are made for the lab by a script with a fixed random seed. `stepped_run.csv` comes from a simulation of the same one-worker service, built for teaching. It is not a recording of your machine or of a real system.
