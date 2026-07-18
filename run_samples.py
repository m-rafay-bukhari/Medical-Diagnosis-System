"""
run_samples.py
Runs Bayesian diagnosis on every patient in sample_patients.json.

Prerequisites (see README.md -> How to Run):
    1. pip install -r requirements.txt
    2. python -m spacy download en_core_web_sm
    3. Neo4j running on bolt://localhost:7687 with credentials in db/connection.py
    4. Knowledge already loaded (run app/main.py once first to populate Neo4j)

Usage:
    python run_samples.py
    python run_samples.py --top 5
    python run_samples.py --input sample_patients.json
"""

import argparse
import json
import sys
from pathlib import Path

from app.bayesian import run_diagnosis


def load_patients(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def render_patient_header(p: dict) -> str:
    return (
        f"{p['patient_id']}  {p['name']}  "
        f"(age {p['age']}, {p['sex']}, {p['city']})\n"
        f"  complaint: {p['chief_complaint']}\n"
        f"  symptoms : {', '.join(s for s, v in p['observed_symptoms'].items() if v == 1)}"
    )


def render_ranked(ranked: list[tuple[str, float]], top: int) -> str:
    if not ranked:
        return "  (no candidate diseases — symptoms may not match the knowledge base)"
    lines = []
    for i, (disease, prob) in enumerate(ranked[:top], start=1):
        lines.append(f"  {i:>2}. {disease:<35} P={prob:.4f}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Bayesian diagnosis on sample patients.")
    parser.add_argument("--input", default="sample_patients.json", help="Path to patients JSON.")
    parser.add_argument("--top", type=int, default=5, help="Show top-k diseases per patient.")
    args = parser.parse_args()

    patients_path = Path(args.input)
    if not patients_path.exists():
        print(f"ERROR: patients file not found: {patients_path}", file=sys.stderr)
        return 1

    patients = load_patients(patients_path)
    print(f"Loaded {len(patients)} patients from {patients_path}\n")
    print("=" * 70)

    for p in patients:
        print(render_patient_header(p))

        # Normalize to {symptom: 0|1}; only forward symptoms where value == 1.
        observed = {s: int(v) for s, v in p["observed_symptoms"].items()}

        try:
            ranked = run_diagnosis(observed)
        except Exception as e:
            print(f"  DIAGNOSIS FAILED: {type(e).__name__}: {e}")
            print("=" * 70)
            continue

        print(f"  top {args.top} diseases (posterior P(Disease | Symptoms)):")
        print(render_ranked(ranked, args.top))
        print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
