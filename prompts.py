# prompts.py
"""
Prompt Library for AI Chat Dataset Pipeline
-------------------------------------------
Centralized prompt templates used across:
- generator.py
- evaluator.py (future LLM scoring)
- fine-tuning pipelines

Author: AI Engineer Pipeline
"""

from typing import Dict, List
import random


# -----------------------------
# SYSTEM PROMPTS
# -----------------------------

SYSTEM_PROMPTS: List[str] = [
    "You are a helpful AI assistant.",
    "You are a highly accurate and concise AI engineer assistant.",
    "You are an expert in Python, AI, and machine learning.",
    "You are a safe and responsible AI assistant that follows instructions carefully.",
]


# -----------------------------
# USER TASK PROMPTS
# -----------------------------

USER_PROMPTS: Dict[str, List[str]] = {
    "ml": [
        "Explain machine learning in simple terms.",
        "What is supervised vs unsupervised learning?",
        "How does a neural network learn?"
    ],
    "deep_learning": [
        "Explain backpropagation step by step.",
        "What are transformers in deep learning?",
        "Why do we use activation functions?"
    ],
    "python": [
        "Write a Python function for binary search.",
        "How do I reverse a linked list in Python?",
        "Explain decorators in Python with example."
    ],
    "interview": [
        "What is overfitting in machine learning?",
        "Explain gradient descent.",
        "What is the bias-variance tradeoff?"
    ]
}


# -----------------------------
# ASSISTANT STYLE PROMPTS
# -----------------------------

ASSISTANT_STYLES: List[str] = [
    "Explain step by step in simple language.",
    "Give a concise but complete explanation.",
    "Provide a technical explanation with examples.",
    "Break it down in beginner-friendly terms."
]


# -----------------------------
# SAFETY PROMPTS (for filtering generation style)
# -----------------------------

SAFE_MODE_INSTRUCTION = (
    "Do not generate harmful, illegal, or unsafe content. "
    "Always keep responses educational and safe."
)


# -----------------------------
# PROMPT BUILDERS
# -----------------------------

def get_system_prompt() -> str:
    """Return a random system prompt."""
    return random.choice(SYSTEM_PROMPTS)


def get_user_prompt(category: str = None) -> str:
    """Return a user prompt from category or random pool."""
    if category and category in USER_PROMPTS:
        return random.choice(USER_PROMPTS[category])
    
    # fallback random across all
    all_prompts = sum(USER_PROMPTS.values(), [])
    return random.choice(all_prompts)


def get_assistant_style() -> str:
    """Return a random assistant style instruction."""
    return random.choice(ASSISTANT_STYLES)


def build_full_prompt(category: str = None) -> Dict[str, str]:
    """
    Build a structured prompt set for dataset generation.
    
    Returns:
        {
            "system": "...",
            "user": "...",
            "style": "..."
        }
    """
    return {
        "system": get_system_prompt(),
        "user": get_user_prompt(category),
        "style": get_assistant_style()
    }


# -----------------------------
# ADVANCED PROMPT VARIANTS
# -----------------------------

def coding_prompt() -> str:
    return "You are a Python expert. Solve coding problems with clean and optimized solutions."


def explanation_prompt() -> str:
    return "You are a teacher AI. Explain concepts clearly with examples and intuition."


def interview_prompt() -> str:
    return "You are a senior AI engineer conducting technical interviews."


# -----------------------------
# PROMPT DEBUG HELPERS
# -----------------------------

def preview_prompt(category: str = None) -> None:
    """Print a sample prompt structure for debugging."""
    prompt = build_full_prompt(category)
    print("\n--- PROMPT PREVIEW ---")
    print(f"System: {prompt['system']}")
    print(f"User: {prompt['user']}")
    print(f"Style: {prompt['style']}")
    print("----------------------\n")