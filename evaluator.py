# evaluator.py
"""
AI Chat Dataset Evaluator
-------------------------
Evaluates generated chat datasets against expected patterns
using heuristic scoring and structural validation.

Future upgrades can include:
- BLEU / ROUGE scoring
- Embedding similarity
- LLM-as-a-judge evaluation

Author: AI Engineer Pipeline
"""

import json
import os
from typing import List, Dict, Any, Tuple


class ChatEvaluator:
    """
    Evaluates AI chat outputs for quality and correctness.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: List[Dict[str, Any]] = []

        self.total_samples = 0
        self.valid_samples = 0
        self.score_sum = 0.0

        self.errors: List[str] = []

    def load_data(self) -> bool:
        """Load JSONL dataset safely."""
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
                        self.data.append(json.loads(line))
                    except json.JSONDecodeError:
                        self.errors.append(f"Line {i}: Invalid JSON")

            return True

        except Exception as e:
            print(f"[ERROR] Failed to read file: {str(e)}")
            return False

    def extract_assistant_text(self, messages: List[Dict[str, str]]) -> str:
        """Extract assistant response safely."""
        for msg in messages:
            if msg.get("role") == "assistant":
                return msg.get("content", "")
        return ""

    def basic_quality_score(self, text: str) -> float:
        """
        Heuristic scoring:
        - Longer, structured answers score higher
        - Penalize empty or too short responses
        """

        if not text or not isinstance(text, str):
            return 0.0

        score = 0.0

        # length factor
        length = len(text.split())
        if length < 5:
            return 0.2

        if length > 50:
            score += 0.4
        else:
            score += 0.2

        # structure bonus
        if "." in text:
            score += 0.2

        if "\n" in text:
            score += 0.2

        return min(score, 1.0)

    def evaluate_sample(self, sample: Dict[str, Any]) -> float:
        """Evaluate one chat sample."""
        messages = sample.get("messages", [])

        if not isinstance(messages, list) or len(messages) == 0:
            return 0.0

        assistant_text = self.extract_assistant_text(messages)

        return self.basic_quality_score(assistant_text)

    def run(self):
        """Run full evaluation pipeline."""

        if not self.load_data():
            return

        self.total_samples = len(self.data)

        if self.total_samples == 0:
            print("[ERROR] No valid data found.")
            return

        for sample in self.data:
            try:
                score = self.evaluate_sample(sample)
                self.score_sum += score
                self.valid_samples += 1
            except Exception as e:
                self.errors.append(str(e))

        self.print_report()

    def print_report(self):
        """Print evaluation summary."""

        avg_score = (
            self.score_sum / self.valid_samples
            if self.valid_samples > 0
            else 0
        )

        print("\n========== EVALUATION REPORT ==========")
        print(f"Total Samples   : {self.total_samples}")
        print(f"Valid Samples   : {self.valid_samples}")
        print(f"Average Score   : {round(avg_score, 4)}")
        print(f"Errors Found    : {len(self.errors)}")

        if self.errors:
            print("\n----- SAMPLE ERRORS (first 10) -----")
            for err in self.errors[:10]:
                print(f"- {err}")

        print("======================================\n")


def main():
    file_path = "generated_chats.jsonl"
    evaluator = ChatEvaluator(file_path)
    evaluator.run()


if __name__ == "__main__":
    main()