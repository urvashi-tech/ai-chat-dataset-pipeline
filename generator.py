# generator.py
"""
AI Chat Dataset Generator
-------------------------
Generates synthetic high-quality chat datasets in JSONL format
for training/evaluation pipelines.

Each sample follows:
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ]
}

Author: AI Engineer Pipeline
"""

import json
import random
import os
from typing import List, Dict, Any


class ChatGenerator:
    """
    Generates structured AI chat datasets.
    """

    def __init__(self, output_file: str, seed: int = 42):
        self.output_file = output_file
        self.seed = seed
        random.seed(seed)

        # Basic seed data (can later be moved to prompts.py)
        self.system_prompts = [
            "You are a helpful AI assistant.",
            "You are an expert AI engineer helping users with coding.",
            "You are a precise and logical assistant."
        ]

        self.user_queries = [
            "Explain machine learning in simple terms.",
            "How does backpropagation work?",
            "Write a Python function for binary search.",
            "What is overfitting in AI models?",
            "Explain transformers in deep learning.",
            "How do I optimize a neural network?",
            "What is gradient descent?"
        ]

        self.assistant_templates = [
            "Sure! {answer}",
            "Let me explain step by step: {answer}",
            "Here is a clear explanation: {answer}",
            "{answer}"
        ]

        self.answer_bank = {
            "machine learning": "Machine learning is a subset of AI where systems learn patterns from data without being explicitly programmed.",
            "backpropagation": "Backpropagation is an algorithm used to update neural network weights by propagating error backward using gradients.",
            "binary search": """def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1""",
            "overfitting": "Overfitting occurs when a model learns training data too well, including noise, and performs poorly on unseen data.",
            "transformers": "Transformers are deep learning models based on self-attention mechanisms used in NLP tasks.",
            "optimization": "Optimization adjusts model weights to minimize loss using methods like gradient descent.",
            "gradient descent": "Gradient descent is an optimization algorithm that minimizes loss by iteratively moving in the direction of steepest descent."
        }

    def get_system_prompt(self) -> str:
        return random.choice(self.system_prompts)

    def get_user_query(self) -> str:
        return random.choice(self.user_queries)

    def generate_answer(self, query: str) -> str:
        query_lower = query.lower()

        for key in self.answer_bank:
            if key in query_lower:
                return self.answer_bank[key]

        return "This is a general AI-generated explanation based on the query."

    def format_assistant_response(self, answer: str) -> str:
        template = random.choice(self.assistant_templates)
        return template.format(answer=answer)

    def create_chat_sample(self) -> Dict[str, Any]:
        """Create one full chat sample."""
        system = self.get_system_prompt()
        user = self.get_user_query()
        answer = self.generate_answer(user)
        assistant = self.format_assistant_response(answer)

        return {
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
                {"role": "assistant", "content": assistant}
            ]
        }

    def generate_dataset(self, num_samples: int):
        """Generate dataset and save to JSONL file."""
        os.makedirs(os.path.dirname(self.output_file) or ".", exist_ok=True)

        try:
            with open(self.output_file, "w", encoding="utf-8") as f:
                for i in range(num_samples):
                    sample = self.create_chat_sample()
                    f.write(json.dumps(sample, ensure_ascii=False) + "\n")

            print(f"[SUCCESS] Generated {num_samples} samples -> {self.output_file}")

        except Exception as e:
            print(f"[ERROR] Failed to generate dataset: {str(e)}")


def main():
    output_path = "generated_chats.jsonl"
    generator = ChatGenerator(output_path)

    # Default dataset size (can be modified later via CLI or config)
    generator.generate_dataset(num_samples=50)


if __name__ == "__main__":
    main()