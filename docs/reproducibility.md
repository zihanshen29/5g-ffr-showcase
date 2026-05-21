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
