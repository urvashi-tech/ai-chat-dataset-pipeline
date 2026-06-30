# safety.py
"""
AI Chat Safety Module
---------------------
Implements rule-based safety checks for AI-generated datasets.

Features:
- Keyword-based toxicity detection
- Basic PII detection (emails, phone numbers)
- Risk scoring system
- Dataset-level safety scanning

Author: AI Engineer Pipeline
"""

import re
import json
import os
from typing import List, Dict, Any, Tuple


class SafetyChecker:
    """
    Safety validation system for AI chat datasets.
    """

    # Basic unsafe keyword categories
    UNSAFE_KEYWORDS = [
        "kill", "murder", "bomb", "terror", "suicide",
        "hack password", "steal", "illegal drugs",
        "hate", "racist", "abuse"
    ]

    EMAIL_PATTERN = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b")
    PHONE_PATTERN = re.compile(r"\b\d{10}\b")

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: List[Dict[str, Any]] = []

        self.total = 0
        self.safe = 0
        self.unsafe = 0

        self.unsafe_samples: List[Tuple[int, str]] = []

    def load_data(self) -> bool:
        """Load JSONL file safely."""
        if not os.path.isfile(self.file_path):
            print(f"[ERROR] File not found: {self.file_path}")
            return False

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                for i, line in enumerate(f, start=1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        self.data.append((i, json.loads(line)))
                    except json.JSONDecodeError:
                        self.unsafe_samples.append((i, "Invalid JSON"))

            return True

        except Exception as e:
            print(f"[ERROR] Failed to read file: {str(e)}")
            return False

    def extract_text(self, sample: Dict[str, Any]) -> str:
        """Extract full conversation text."""
        messages = sample.get("messages", [])
        text = ""

        for msg in messages:
            content = msg.get("content", "")
            if isinstance(content, str):
                text += " " + content.lower()

        return text

    def keyword_risk(self, text: str) -> float:
        """Check unsafe keyword presence."""
        risk = 0.0

        for kw in self.UNSAFE_KEYWORDS:
            if kw in text:
                risk += 0.2

        return min(risk, 1.0)

    def pii_risk(self, text: str) -> float:
        """Detect PII leaks."""
        risk = 0.0

        if self.EMAIL_PATTERN.search(text):
            risk += 0.5

        if self.PHONE_PATTERN.search(text):
            risk += 0.5

        return min(risk, 1.0)

    def compute_risk(self, sample: Dict[str, Any]) -> float:
        """Compute total safety risk score."""
        text = self.extract_text(sample)

        keyword_r = self.keyword_risk(text)
        pii_r = self.pii_risk(text)

        return min(keyword_r + pii_r, 1.0)

    def is_safe(self, risk: float, threshold: float = 0.5) -> bool:
        """Determine if sample is safe."""
        return risk < threshold

    def run(self, threshold: float = 0.5):
        """Run full safety scan."""

        if not self.load_data():
            return

        self.total = len(self.data)

        for line_num, sample in self.data:
            try:
                risk = self.compute_risk(sample)

                if self.is_safe(risk, threshold):
                    self.safe += 1
                else:
                    self.unsafe += 1
                    self.unsafe_samples.append((line_num, f"Risk={risk}"))

            except Exception as e:
                self.unsafe_samples.append((line_num, f"Error: {str(e)}"))

        self.print_report()

    def print_report(self):
        """Print safety summary."""

        print("\n========== SAFETY REPORT ==========")
        print(f"Total Samples : {self.total}")
        print(f"Safe Samples  : {self.safe}")
        print(f"Unsafe Samples: {self.unsafe}")
        print(f"Flagged Items : {len(self.unsafe_samples)}")

        if self.unsafe_samples:
            print("\n----- FLAGGED SAMPLES (first 10) -----")
            for item in self.unsafe_samples[:10]:
                print(f"- Line {item[0]}: {item[1]}")

        print("===================================\n")


def main():
    file_path = "generated_chats.jsonl"
    checker = SafetyChecker(file_path)
    checker.run()


if __name__ == "__main__":
    main()