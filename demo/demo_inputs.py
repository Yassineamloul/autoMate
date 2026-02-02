"""Hardcoded demo scenarios for the policy automation agent."""
from pathlib import Path


def sample_paths():
    base = Path(__file__).parent / "sample_policies"
    return [base / "employee_handbook.pdf", base / "travel_policy.pdf"]
