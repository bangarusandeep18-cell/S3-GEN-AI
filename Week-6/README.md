# Week 6 - Generative AI Programming Practical

**Experiment:** Golden Question Set and First Llama 3.2 Baseline Run  
**Release:** v0.1

## Project files

- `main.py` - sends each question to the local Ollama API, computes keyword coverage, and prints a baseline summary.
- `golden_set.json` - 30 questions with expected answers, keywords, and sources.
- `requirements.txt` - Python dependency (`requests`).
- `.gitignore` - excludes the virtual environment and Python cache.

## 1. Install / verify Ollama

Open PowerShell and check that Ollama is available:

```powershell
ollama --version
```

Download the Llama 3.2 model:

```powershell
ollama pull llama3.2
```

Start the Ollama application/service before running the Python script. To verify that the model is available, use:

```powershell
ollama list
```

The program uses the local endpoint `http://localhost:11434/api/generate` and model name `llama3.2`.

## 2. Set up Python in VS Code

Open this `Week-6` folder in VS Code. In **Terminal > New Terminal**, run:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks environment activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

> The correct installation command is `pip install -r requirements.txt` (not `pip install requirements.py`).

## 3. Run the first baseline

Make sure Ollama is running and Llama 3.2 has been pulled, then execute:

```powershell
python main.py
```

The program processes all 30 questions. For each response it displays the LLM answer, expected answer, matched keywords, missing keywords, score, and PASS/REVIEW status.

## 4. Output file

The run creates `baseline_results.csv` in this folder. It records the question ID, question, expected answer, LLM answer, matched and missing keywords, score, status, source, model, and release version.

The keyword score is calculated as:

`(number of matched expected keywords / number of expected keywords) * 100`

A score of 60% or higher is labelled `PASS`; a lower score is labelled `REVIEW`. A connection/request failure is recorded as `ERROR`. These are keyword-coverage checks, not a full semantic assessment of answer correctness.

## 5. GitHub note

`baseline_results.csv` is generated when you run the program. If the practical submission requires your baseline evidence, add the CSV to GitHub after you have run the model locally. Do not submit invented scores or an unverified result file.
