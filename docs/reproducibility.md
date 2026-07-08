# Reproducibility Notes

Run the full local workflow:

```bash
python scripts/run_paper_alignment.py
python scripts/verify_paper_trends.py
python scripts/generate_figures.py
pytest
```

Outputs are regenerated from source and a fixed random seed. The generated files under `outputs/` are disposable artifacts and can be removed before publishing a clean repository snapshot.

No private MATLAB scripts, local account paths, school network details, credentials, or raw unpublished materials are required for this public demo.

The public workflow deliberately separates three layers: the first-author review paper, the private MATLAB reproduction of 19-cell strategy trends, and this synthetic Python showcase. Numeric reproduction results quoted in the README are text references from the private MATLAB run in 2026-07; generated CSV/JSON/PNG files in this repository remain synthetic demo artifacts.
