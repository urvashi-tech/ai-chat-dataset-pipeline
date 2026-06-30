# utils.py
"""
Utility functions for AI Chat Dataset Pipeline
----------------------------------------------
Common helpers used across:
- generator.py
- checker.py
- evaluator.py
- safety.py

Author: AI Engineer Pipeline
"""

import json
import os
import sys
import time
from typing import List, Dict, Any, Generator


# -----------------------------
# FILE UTILITIES
# -----------------------------

def file_exists(path: str) -> bool:
    """Check if file exists."""
    return os.path.isfile(path)


def read_jsonl(path: str) -> List[Dict[str, Any]]:
    """Read JSONL file safely."""
    data = []

    if not file_exists(path):
        print(f"[ERROR] File not found: {path}")
        return data

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"[ERROR] Failed reading file: {str(e)}")

    return data


def write_jsonl(path: str, data: List[Dict[str, Any]]) -> None:
    """Write list of dictionaries to JSONL file."""
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        print(f"[SUCCESS] Written {len(data)} records to {path}")

    except Exception as e:
        print(f"[ERROR] Failed writing file: {str(e)}")


# -----------------------------
# LOGGING UTILITIES
# -----------------------------

def log_info(message: str) -> None:
    print(f"[INFO] {message}")


def log_error(message: str) -> None:
    print(f"[ERROR] {message}")


def log_success(message: str) -> None:
    print(f"[SUCCESS] {message}")


# -----------------------------
# PROGRESS UTILITIES
# -----------------------------

def progress_bar(current: int, total: int, bar_length: int = 30) -> None:
    """Simple console progress bar."""
    if total == 0:
        return

    percent = current / total
    filled_length = int(bar_length * percent)

    bar = "█" * filled_length + "-" * (bar_length - filled_length)

    sys.stdout.write(f"\rProgress: |{bar}| {int(percent*100)}%")
    sys.stdout.flush()

    if current == total:
        print()


# -----------------------------
# TIME UTILITIES
# -----------------------------

def current_timestamp() -> str:
    """Return current timestamp as string."""
    return time.strftime("%Y-%m-%d %H:%M:%S")


def elapsed_time(start: float) -> str:
    """Return elapsed time in seconds."""
    return f"{round(time.time() - start, 2)}s"


# -----------------------------
# DATA VALIDATION HELPERS
# -----------------------------

def is_valid_json(obj: Any) -> bool:
    """Check if object is JSON serializable."""
    try:
        json.dumps(obj)
        return True
    except Exception:
        return False


def safe_get(dictionary: Dict[str, Any], key: str, default=None):
    """Safe dictionary getter."""
    if not isinstance(dictionary, dict):
        return default
    return dictionary.get(key, default)


# -----------------------------
# ITERATION HELPERS
# -----------------------------

def chunk_list(data: List[Any], chunk_size: int) -> Generator[List[Any], None, None]:
    """Yield chunks from a list."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]