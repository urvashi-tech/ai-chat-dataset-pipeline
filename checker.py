# checker.py
"""
AI Chat Dataset Checker
-----------------------
Validates JSONL chat datasets for format correctness, missing fields,
and structural issues before training/evaluation.

Author: AI Engineer Pipeline
"""

import json
import os
import sys
from typing import Dict, List, Any, Tuple


class ChatDatasetChecker:
    """
    A professional checker for AI chat datasets in JSONL format.
    Each line must contain a valid JSON object with a 'messages' field.
    """

    REQUIRED_TOP_LEVEL_KEYS = ["messages"]

    REQUIRED_MESSAGE_KEYS = ["role", "content"]

    ALLOWED_ROLES = {"system", "user", "assistant"}

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.errors: List[str] = []
        self.total_lines = 0
        self.valid_lines = 0

    def file_exists(self) -> bool:
        """Check if dataset file exists."""
        return os.path.isfile(self.file_path)

    def read_lines(self) -> List[str]:
        """Read all lines safely from file."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return f.readlines()
        except Exception as e:
            self.errors.append(f"Failed to read file: {str(e)}")
            return []

    def validate_json(self, line: str, line_num: int) -> Tuple[bool, Any]:
        """Validate JSON parsing."""
        try:
            return True, json.loads(line)
        except json.JSONDecodeError as e:
            self.errors.append(f"Line {line_num}: Invalid JSON - {str(e)}")
            return False, None

    def validate_structure(self, obj: Dict[str, Any], line_num: int) -> bool:
        """Validate top-level structure."""
        if not isinstance(obj, dict):
            self.errors.append(f"Line {line_num}: Root element must be a JSON object")
            return False

        for key in self.REQUIRED_TOP_LEVEL_KEYS:
            if key not in obj:
                self.errors.append(f"Line {line_num}: Missing key '{key}'")
                return False

        if not isinstance(obj["messages"], list):
            self.errors.append(f"Line {line_num}: 'messages' must be a list")
            return False

        return True

    def validate_messages(self, messages: List[Dict[str, Any]], line_num: int) -> bool:
        """Validate message list structure."""
        if len(messages) == 0:
            self.errors.append(f"Line {line_num}: 'messages' cannot be empty")
            return False

        for i, msg in enumerate(messages):
            if not isinstance(msg, dict):
                self.errors.append(f"Line {line_num}: Message {i} is not an object")
                return False

            for key in self.REQUIRED_MESSAGE_KEYS:
                if key not in msg:
                    self.errors.append(
                        f"Line {line_num}: Message {i} missing '{key}'"
                    )
                    return False

            if msg["role"] not in self.ALLOWED_ROLES:
                self.errors.append(
                    f"Line {line_num}: Message {i} has invalid role '{msg['role']}'"
                )
                return False

            if not isinstance(msg["content"], str):
                self.errors.append(
                    f"Line {line_num}: Message {i} content must be a string"
                )
                return False

        return True

    def validate_line(self, line: str, line_num: int) -> bool:
        """Validate a single JSONL line."""
        line = line.strip()

        if not line:
            return False

        is_valid_json, obj = self.validate_json(line, line_num)
        if not is_valid_json:
            return False

        if not self.validate_structure(obj, line_num):
            return False

        if not self.validate_messages(obj["messages"], line_num):
            return False

        return True

    def run(self) -> bool:
        """Run full dataset validation."""
        if not self.file_exists():
            print(f"[ERROR] File not found: {self.file_path}")
            return False

        lines = self.read_lines()

        if not lines:
            print("[ERROR] File is empty or unreadable.")
            return False

        self.total_lines = len(lines)

        for i, line in enumerate(lines, start=1):
            if self.validate_line(line, i):
                self.valid_lines += 1

        self.print_report()
        return len(self.errors) == 0

    def print_report(self):
        """Print validation summary."""
        print("\n========== DATASET VALIDATION REPORT ==========")
        print(f"Total Lines   : {self.total_lines}")
        print(f"Valid Lines   : {self.valid_lines}")
        print(f"Invalid Lines : {len(self.errors)}")

        if self.errors:
            print("\n----- ERRORS (First 20) -----")
            for err in self.errors[:20]:
                print(f"- {err}")

        print("==============================================\n")


def main():
    if len(sys.argv) != 2:
        print("Usage: python checker.py <dataset.jsonl>")
        sys.exit(1)

    file_path = sys.argv[1]
    checker = ChatDatasetChecker(file_path)

    is_valid = checker.run()

    if not is_valid:
        sys.exit(1)


if __name__ == "__main__":
    main()