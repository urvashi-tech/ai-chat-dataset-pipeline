# config.py
"""
Configuration file for AI Chat Dataset Pipeline
------------------------------------------------
Central place for all project settings:
- File paths
- Dataset parameters
- Safety thresholds
- Evaluation settings

Author: AI Engineer Pipeline
"""

import os
from dataclasses import dataclass


# -----------------------------
# BASE PROJECT CONFIG
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# -----------------------------
# DATASET PATHS
# -----------------------------

DATA_DIR = os.path.join(BASE_DIR)

GENERATED_DATA_PATH = os.path.join(DATA_DIR, "generated_chats.jsonl")
CHECKED_DATA_PATH = os.path.join(DATA_DIR, "checked_chats.jsonl")
RESULTS_CSV_PATH = os.path.join(DATA_DIR, "results.csv")

SAMPLE_CHATS_PATH = os.path.join(DATA_DIR, "sample_chats.jsonl")


# -----------------------------
# GENERATION SETTINGS
# -----------------------------

@dataclass
class GenerationConfig:
    num_samples: int = 50
    seed: int = 42
    max_turns: int = 3  # system + user + assistant style
    include_system: bool = True


GEN_CONFIG = GenerationConfig()


# -----------------------------
# SAFETY SETTINGS
# -----------------------------

@dataclass
class SafetyConfig:
    risk_threshold: float = 0.5
    enable_pii_check: bool = True
    enable_keyword_filter: bool = True


SAFETY_CONFIG = SafetyConfig()


# -----------------------------
# EVALUATION SETTINGS
# -----------------------------

@dataclass
class EvaluationConfig:
    min_length_score: float = 0.2
    max_length_bonus: float = 0.4
    structure_bonus: float = 0.4


EVAL_CONFIG = EvaluationConfig()


# -----------------------------
# LOGGING SETTINGS
# -----------------------------

LOGGING_ENABLED = True
VERBOSE = True


# -----------------------------
# HELPER FUNCTIONS
# -----------------------------

def print_config():
    """Print current configuration (debugging)."""
    print("\n========== CONFIGURATION ==========")
    print(f"Generated Data Path : {GENERATED_DATA_PATH}")
    print(f"Checked Data Path   : {CHECKED_DATA_PATH}")
    print(f"Results CSV Path    : {RESULTS_CSV_PATH}")
    print(f"Num Samples         : {GEN_CONFIG.num_samples}")
    print(f"Safety Threshold    : {SAFETY_CONFIG.risk_threshold}")
    print("===================================\n")