"""Run the synthetic paper-alignment sweep."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from ffr_showcase.simulation import write_alignment_outputs


def main() -> None:
    output_dir = Path(__file__).resolve().parents[1] / "outputs"
    csv_path = write_alignment_outputs(output_dir)
    print(f"Wrote synthetic alignment results: {csv_path}")


if __name__ == "__main__":
    main()
