import csv
import json
from datetime import datetime
from pathlib import Path

import requests

# STEP 1: CONFIGURATION
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "golden_set.json"
OUTPUT_FILE = BASE_DIR / "baseline_results.csv"


def load_golden_questions():
    """Load the prepared golden question set from JSON."""
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        questions = json.load(file)

    if not isinstance(questions, list):
        raise ValueError("golden_set.json must contain a JSON list.")
    if not questions:
        raise ValueError("golden_set.json does not contain any questions.")
    return questions


def get_llm_answer(question):
    """Send one prompt to the local Ollama generate endpoint."""
    payload = {
        "model": MODEL_NAME,
        "prompt": question,
        "stream": False,
        "options": {"temperature": 0},
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    result = response.json()
    return result.get("response", "").strip()


def calculate_score(answer, expected_keywords):
    """Return keyword coverage percentage and matched/missing keywords."""
    answer_lower = answer.lower()
    matched_keywords = []
    missing_keywords = []

    for keyword in expected_keywords:
        if keyword.lower() in answer_lower:
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    total_keywords = len(expected_keywords)
    score = (len(matched_keywords) / total_keywords * 100) if total_keywords else 0

    return round(score, 2), matched_keywords, missing_keywords


def run_baseline(golden_questions):
    """Evaluate every golden question and collect one result per question."""
    results = []
    total_score = 0.0
    successful_questions = 0

    print("\n======================================")
    print("BASELINE RUN STARTED")
    print("======================================")

    for index, item in enumerate(golden_questions, start=1):
        question_id = item["id"]
        question = item["question"]
        expected_answer = item["expected_answer"]
        keywords = item["keywords"]
        source = item["source"]

        print("\n--------------------------------------")
        print(f"Question {index}: {question_id}")
        print("Question:", question)

        try:
            answer = get_llm_answer(question)
            score, matched, missing = calculate_score(answer, keywords)
            status = "PASS" if score >= 60 else "REVIEW"

            total_score += score
            successful_questions += 1

            print("\nLLM Answer:")
            print(answer)
            print("\nExpected Answer:")
            print(expected_answer)
            print("\nMatched Keywords:", matched)
            print("Missing Keywords:", missing)
            print("Score:", score, "%")
            print("Status:", status)

            results.append({
                "Question_ID": question_id,
                "Question": question,
                "Expected_Answer": expected_answer,
                "LLM_Answer": answer,
                "Matched_Keywords": ", ".join(matched),
                "Missing_Keywords": ", ".join(missing),
                "Score": score,
                "Status": status,
                "Source": source,
                "Model": MODEL_NAME,
                "Release": "v0.1",
            })

        except requests.RequestException as error:
            print("Ollama request error:", error)
            results.append({
                "Question_ID": question_id,
                "Question": question,
                "Expected_Answer": expected_answer,
                "LLM_Answer": "",
                "Matched_Keywords": "",
                "Missing_Keywords": ", ".join(keywords),
                "Score": 0,
                "Status": "ERROR",
                "Source": source,
                "Model": MODEL_NAME,
                "Release": "v0.1",
            })
        except (KeyError, TypeError) as error:
            print("Golden-set data error:", error)
            results.append({
                "Question_ID": question_id,
                "Question": question,
                "Expected_Answer": expected_answer,
                "LLM_Answer": "",
                "Matched_Keywords": "",
                "Missing_Keywords": ", ".join(keywords),
                "Score": 0,
                "Status": "ERROR",
                "Source": source,
                "Model": MODEL_NAME,
                "Release": "v0.1",
            })

    return results, total_score, successful_questions


def save_results(results):
    """Write the baseline evaluation results to a CSV file."""
    fieldnames = [
        "Question_ID",
        "Question",
        "Expected_Answer",
        "LLM_Answer",
        "Matched_Keywords",
        "Missing_Keywords",
        "Score",
        "Status",
        "Source",
        "Model",
        "Release",
    ]

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def print_summary(golden_questions, results, total_score, successful_questions):
    """Print the v0.1 baseline summary."""
    average_score = total_score / successful_questions if successful_questions else 0
    passed = sum(result["Status"] == "PASS" for result in results)
    review = sum(result["Status"] == "REVIEW" for result in results)
    errors = sum(result["Status"] == "ERROR" for result in results)

    print("\n======================================")
    print("BASELINE EVALUATION SUMMARY")
    print("======================================")
    print("Release Version: v0.1")
    print("Model:", MODEL_NAME)
    print("Total Questions:", len(golden_questions))
    print("Successful Responses:", successful_questions)
    print("Passed Questions:", passed)
    print("Questions for Review:", review)
    print("Failed Requests:", errors)
    print("Average Keyword Coverage:", round(average_score, 2), "%")
    print("Evaluation Date:", datetime.now().isoformat(timespec="seconds"))


def main():
    try:
        golden_questions = load_golden_questions()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print("Could not load golden question set:", error)
        return

    print("\n======================================")
    print("GOLDEN QUESTION SET")
    print("======================================")
    print("Total Questions:", len(golden_questions))
    print("Model:", MODEL_NAME)

    results, total_score, successful_questions = run_baseline(golden_questions)
    save_results(results)
    print_summary(golden_questions, results, total_score, successful_questions)

    print("\nResults saved to:", OUTPUT_FILE.name)
    print("\nBASELINE RUN COMPLETED!")
    print("Release v0.1 created successfully.")


if __name__ == "__main__":
    main()
