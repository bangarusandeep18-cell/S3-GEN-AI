# Week 5 - Token Economics: Cost and Rate-Limit Budgeting

## Aim

Build a small Python budgeting tool that estimates token usage and hosted API
cost, checks expected traffic against RPM/TPM limits, and reports whether the
feature is within its configured daily and monthly budget.

## Files

- `main.py` - convenient program entry point
- `budget.py` - budget calculations and report generation
- `test_budget.py` - automated unit tests
- `requirements.txt` - Python dependency list
- `.env.example` - sample configuration values
- `.gitignore` - excludes the local `.env`, virtual environment, and cache files

## Setup in VS Code (Windows PowerShell)

Open this `Week-5` folder in VS Code, then open **Terminal > New Terminal**.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

## Run the program

```bash
python main.py
```

## Run the tests

```bash
python -m unittest -v
```

The test suite includes checks for cost estimates, capacity checks, RPM-limit
failure, monthly-budget failure, and rejection of negative usage assumptions.

## What-if analysis

Edit one setting at a time in `.env`, save, and run `python main.py` again.

- Double `REQUESTS_PER_DAY` from 2000 to 4000.
- Increase `AVG_INPUT_TOKENS` to represent a longer context.
- Increase `AVG_OUTPUT_TOKENS` to represent longer answers.
- Increase `PEAK_REQUESTS_PER_MINUTE` until an RPM or TPM check requires review.
- Reduce `AVG_INPUT_TOKENS` to represent prompt reduction.

Restore the sample values after experimenting.

## Important

The prices and rate limits in `.env.example` are illustrative lab values, not
live provider prices or guaranteed quotas. Verify current prices and limits for
the selected model, account, and service tier before a real launch. The report
is a planning estimate, not a billing guarantee.
