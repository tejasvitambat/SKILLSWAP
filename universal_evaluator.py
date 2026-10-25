"""
SkillSwap Universal Task Evaluator
=================================

Purpose:
    One evaluation engine for coding and non-coding roadmap tasks.

Supported task types:
    coding
    speaking
    creative
    marketing
    practical

Important:
    - This module does NOT modify the database.
    - It does NOT delete or change learner progress.
    - The submit route should call evaluate_submission(...)
      and then save the returned result.
    - Coding execution is intentionally conservative. Never execute
      untrusted submissions in the production Flask process without
      an isolated sandbox/container.
"""

from __future__ import annotations

import ast
import io
import re
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout
from typing import Dict, List, Tuple


# ============================================================
# RESULT HELPERS
# ============================================================

def result(passed: bool, score: int, feedback: str) -> Tuple[bool, int, str]:
    score = max(0, min(100, int(score)))
    return passed, score, feedback


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def words(text: str) -> List[str]:
    return re.findall(r"[A-Za-z0-9_+#.-]+", text or "")


# ============================================================
# CODING EVALUATION
# ============================================================

LANGUAGE_ALIASES = {
    "python": "python",
    "py": "python",
    "java": "java",
    "javascript": "javascript",
    "js": "javascript",
    "c++": "cpp",
    "cpp": "cpp",
    "sql": "sql",
}


def detect_code_language(topic) -> str:
    """
    Detect language from:
        1. topic title
        2. topic code_example
        3. task_type

    The seed currently stores coding topics under task_type='coding',
    so the actual language is inferred from roadmap/topic content.
    """
    title = normalize(getattr(topic, "title", ""))
    example = normalize(getattr(topic, "code_example", ""))

    combined = f"{title} {example}"

    for key, value in LANGUAGE_ALIASES.items():
        if key in combined:
            return value

    # Python is the safest legacy fallback because the previous
    # evaluator was Python-specific.
    return "python"


def evaluate_python(code: str) -> Tuple[bool, int, str]:
    if not code.strip():
        return result(False, 0, "Submit a Python solution.")

    try:
        tree = ast.parse(code)
    except SyntaxError as exc:
        return result(False, 0, f"Python syntax error: {exc.msg} on line {exc.lineno}.")

    node_count = sum(1 for _ in ast.walk(tree))

    if node_count < 2:
        return result(False, 20, "Your solution is too small. Add the required Python logic.")

    # Compile first; do not execute obviously dangerous modules/functions.
    dangerous = {
        "os", "sys", "subprocess", "socket", "shutil",
        "pathlib", "requests", "urllib", "ctypes",
    }

    imported = set()
    calls = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".")[0])
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.add(node.func.id)

    blocked = dangerous.intersection(imported)
    if blocked:
        return result(
            False,
            0,
            "The submission uses restricted modules. Use the Python concepts taught in this topic."
        )

    try:
        compile(tree, "<skillswap-submission>", "exec")
    except Exception as exc:
        return result(False, 0, f"Python compilation failed: {exc}")

    score = 55

    if any(isinstance(n, ast.Assign) for n in ast.walk(tree)):
        score += 10
    if any(isinstance(n, ast.If) for n in ast.walk(tree)):
        score += 10
    if any(isinstance(n, ast.For) for n in ast.walk(tree)):
        score += 10
    if any(isinstance(n, ast.While) for n in ast.walk(tree)):
        score += 5
    if "print" in calls:
        score += 10

    return result(
        score >= 70,
        score,
        "Python syntax and basic structure are valid. "
        + ("The task passed the universal coding checks."
           if score >= 70 else
           "Add more of the required logic before submitting again.")
    )


def evaluate_java(code: str) -> Tuple[bool, int, str]:
    text = code.strip()

    if not text:
        return result(False, 0, "Submit a Java solution.")

    score = 25
    checks = []

    if re.search(r"\bclass\s+\w+", text):
        score += 20
        checks.append("class declaration")
    if re.search(r"\bpublic\s+static\s+void\s+main\s*\(", text):
        score += 25
        checks.append("main method")
    if re.search(r"\b(int|double|float|String|boolean)\b", text):
        score += 10
        checks.append("typed data")
    if "System.out" in text:
        score += 10
        checks.append("output")
    if ";" in text:
        score += 10
        checks.append("Java statements")

    if score >= 70:
        return result(True, score, "Java structure passed the universal checks.")
    return result(
        False,
        score,
        "Java submission needs more required structure. "
        "Expected elements may include a class, main method, typed data and output."
    )


def evaluate_javascript(code: str) -> Tuple[bool, int, str]:
    text = code.strip()

    if not text:
        return result(False, 0, "Submit a JavaScript solution.")

    score = 25

    if re.search(r"\b(let|const|var)\b", text):
        score += 15
    if re.search(r"\bfunction\b|=>", text):
        score += 20
    if re.search(r"\b(if|for|while|switch)\b", text):
        score += 15
    if re.search(r"\b(console\.log|document\.|return)\b", text):
        score += 15
    if re.search(r"[{}();]", text):
        score += 10

    if score >= 70:
        return result(True, score, "JavaScript structure passed the universal checks.")
    return result(
        False,
        score,
        "Add the JavaScript concepts required by this topic, then submit again."
    )


def evaluate_cpp(code: str) -> Tuple[bool, int, str]:
    text = code.strip()

    if not text:
        return result(False, 0, "Submit a C++ solution.")

    score = 20

    if re.search(r"#include\s*<", text):
        score += 15
    if re.search(r"\bint\s+main\s*\(", text):
        score += 25
    if re.search(r"\b(int|double|float|char|string|bool)\b", text):
        score += 15
    if "cout" in text or "cin" in text:
        score += 10
    if re.search(r"\b(if|for|while|switch)\b", text):
        score += 10

    if score >= 70:
        return result(True, score, "C++ structure passed the universal checks.")
    return result(
        False,
        score,
        "Add the required C++ structure and logic before submitting again."
    )


def evaluate_sql(code: str) -> Tuple[bool, int, str]:
    text = code.strip()

    if not text:
        return result(False, 0, "Submit a SQL query.")

    upper = text.upper()
    score = 25

    if "SELECT " in upper:
        score += 25
    if "FROM " in upper:
        score += 15
    if "WHERE " in upper:
        score += 10
    if "ORDER BY " in upper or "GROUP BY " in upper:
        score += 10
    if "JOIN " in upper:
        score += 10

    # Basic balance check catches many malformed submissions.
    if text.count("(") == text.count(")"):
        score += 5

    if score >= 70:
        return result(True, score, "SQL structure passed the universal query checks.")
    return result(
        False,
        score,
        "The SQL query needs more of the concepts required by this topic."
    )


def evaluate_coding(topic, submission: str):
    language = detect_code_language(topic)

    evaluators = {
        "python": evaluate_python,
        "java": evaluate_java,
        "javascript": evaluate_javascript,
        "cpp": evaluate_cpp,
        "sql": evaluate_sql,
    }

    return evaluators[language](submission)


# ============================================================
# NON-CODING EVALUATION
# ============================================================

def evaluate_language(topic, submission: str):
    """
    Text-based language-task evaluator.

    It checks:
        - minimum meaningful response length
        - sentence/word structure
        - topic-relevant vocabulary
        - evidence of completion

    This is intentionally not presented as pronunciation or accent
    detection because the current database submission field is Text.
    """

    text = submission.strip()
    token_list = words(text)

    if len(token_list) < 15:
        return result(
            False,
            25,
            "Your language response is too short. Give a complete practical response with examples."
        )

    score = 45

    if len(token_list) >= 30:
        score += 15
    if len(token_list) >= 60:
        score += 10

    sentence_count = len(re.findall(r"[.!?]+", text))
    if sentence_count >= 2:
        score += 10

    title_words = {
        w for w in words(getattr(topic, "title", ""))
        if len(w) >= 4
    }

    response_lower = normalize(text)
    if title_words and any(w in response_lower for w in title_words):
        score += 10

    if score >= 70:
        return result(
            True,
            score,
            "Language task completed with a sufficiently detailed practical response."
        )

    return result(
        False,
        score,
        "Expand your response with clearer sentences, examples and topic-specific usage."
    )


def evaluate_creative(topic, submission: str):
    """
    Creative tasks are evaluated from the submitted written evidence/link.

    The current TaskSubmission schema stores Text only, so the evaluator
    cannot inspect an uploaded image/video directly. It therefore checks
    whether the learner documented the required creative decisions,
    process and final output.
    """

    text = submission.strip()
    if len(words(text)) < 30:
        return result(
            False,
            30,
            "Describe your creative work in more detail. Include process, decisions and final result."
        )

    score = 45
    lower = normalize(text)

    evidence_terms = [
        "process", "design", "choice", "reason",
        "result", "final", "improve", "audience",
    ]

    score += min(30, sum(5 for term in evidence_terms if term in lower))

    if "http://" in lower or "https://" in lower:
        score += 10

    if re.search(r"\b(final|output|deliverable|prototype|mockup|poster|video|photo)\b", lower):
        score += 10

    if score >= 70:
        return result(
            True,
            score,
            "Creative task passed the evidence-based evaluation. "
            "Your submission documents the work and final outcome."
        )

    return result(
        False,
        score,
        "Add stronger evidence: explain your process, decisions, audience, final output and improvements."
    )


def evaluate_marketing(topic, submission: str):
    text = submission.strip()
    if len(words(text)) < 30:
        return result(
            False,
            25,
            "Marketing submission is too short. Provide strategy, audience, action and expected outcome."
        )

    lower = normalize(text)
    score = 40

    criteria = {
        "audience": 15,
        "goal": 10,
        "strategy": 10,
        "content": 10,
        "result": 10,
        "metric": 10,
        "call to action": 5,
    }

    for term, points in criteria.items():
        if term in lower:
            score += points

    if score >= 70:
        return result(
            True,
            score,
            "Marketing task passed the structured strategy evaluation."
        )

    return result(
        False,
        score,
        "Include the target audience, goal, strategy, execution/content, "
        "measurement and expected result."
    )


def evaluate_practical(topic, submission: str):
    text = submission.strip()

    if len(words(text)) < 25:
        return result(
            False,
            25,
            "Provide a complete practical response with what you did, how you did it and the result."
        )

    lower = normalize(text)
    score = 45

    for term in ("steps", "process", "result", "example", "reason", "improve"):
        if term in lower:
            score += 8

    if re.search(r"\d+", text):
        score += 5

    if score >= 70:
        return result(
            True,
            score,
            "Practical task passed the universal evidence-based evaluation."
        )

    return result(
        False,
        score,
        "Add concrete steps, an example, the result and what you would improve."
    )


# ============================================================
# UNIVERSAL DISPATCHER
# ============================================================

def evaluate_submission(topic, submission: str):
    """
    Main public API used by Flask.

    Returns:
        (passed: bool, score: int, feedback: str)
    """

    task_type = normalize(getattr(topic, "task_type", "") or "practical")

    if task_type == "coding":
        return evaluate_coding(topic, submission)

    if task_type == "speaking":
        return evaluate_language(topic, submission)

    if task_type == "creative":
        return evaluate_creative(topic, submission)

    if task_type == "marketing":
        return evaluate_marketing(topic, submission)

    return evaluate_practical(topic, submission)
