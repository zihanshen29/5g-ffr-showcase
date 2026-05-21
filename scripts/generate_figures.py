"""Generate paper-style figures from synthetic FFR alignment data."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ffr_showcase.figures import generate_figures
from ffr_showcase.simulation import write_alignment_outputs


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    output_dir = repo_root / "outputs"
    csv_path = output_dir / "paper_alignment_synthetic.csv"
    if not csv_path.exists():
        csv_path = write_alignment_outputs(output_dir)
    paths = generate_figures(output_dir, csv_path)
    for path in paths:
        print(f"Wrote figure: {path}")


if __name__ == "__main__":
    main()
