"""
Run Pipeline - AI Chat Dataset System
-------------------------------------
This is the MASTER file that connects the entire pipeline:

1. Generate dataset
2. Validate dataset
3. Safety check
4. Evaluate quality
5. Save final outputs

Author: AI Engineer Pipeline
"""

import subprocess
import sys
import time
import os

from config import GENERATED_DATA_PATH


def run_command(command: str, step_name: str):
    """Run shell command safely with logging."""
    print(f"\n🚀 STEP: {step_name}")
    print(f"Running: {command}\n")

    start_time = time.time()

    result = subprocess.run(command, shell=True)

    end_time = time.time()

    if result.returncode != 0:
        print(f"❌ ERROR in {step_name}")
        sys.exit(1)

    print(f"✅ Completed: {step_name} in {round(end_time - start_time, 2)}s")


def file_check(path: str):
    """Check if file exists before next step."""
    if not os.path.exists(path):
        print(f"❌ Missing file: {path}")
        sys.exit(1)
    print(f"📁 Found: {path}")


def main():
    print("\n==============================")
    print("🤖 AI CHAT PIPELINE STARTED")
    print("==============================\n")

    # Step 1: Generate dataset
    run_command("python generator.py", "DATA GENERATION")

    file_check(GENERATED_DATA_PATH)

    # Step 2: Validate dataset
    run_command(f"python checker.py {GENERATED_DATA_PATH}", "DATA VALIDATION")

    # Step 3: Safety check
    run_command("python safety.py", "SAFETY CHECK")

    # Step 4: Evaluation
    run_command("python evaluator.py", "MODEL EVALUATION")

    print("\n==============================")
    print("🎉 PIPELINE COMPLETED SUCCESSFULLY")
    print("==============================\n")

    print("📊 Outputs generated:")
    print("- generated_chats.jsonl")
    print("- safety report (console)")
    print("- evaluation report (console)")
    print("- results.csv (if extended later)")


if __name__ == "__main__":
    main()