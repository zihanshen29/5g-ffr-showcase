"""Verify qualitative trends in the synthetic FFR alignment output."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ffr_showcase.simulation import write_alignment_outputs
from ffr_showcase.trends import verify_trends


def main() -> None:
    output_dir = Path(__file__).resolve().parents[1] / "outputs"
    csv_path = output_dir / "paper_alignment_synthetic.csv"
    if not csv_path.exists():
        csv_path = write_alignment_outputs(output_dir)
    checks = verify_trends(csv_path)
    for name, passed in checks.items():
        print(f"{name}: {'PASS' if passed else 'FAIL'}")
    if not checks["all_passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
