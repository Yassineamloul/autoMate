"""Entry point for demo pipeline."""
from pipelines.ingest_pipeline import run_ingest_demo


def main():
    print("Running policy-automation-agent demo pipeline...")
    run_ingest_demo()


if __name__ == "__main__":
    main()
