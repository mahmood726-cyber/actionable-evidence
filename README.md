<!-- sentinel:skip-file — hardcoded paths are fixture/registry/audit-narrative data for this repo's research workflow, not portable application configuration. Same pattern as push_all_repos.py and E156 workbook files. -->

# ActionableEvidence

ActionableEvidence computes GO / NO-GO verdicts for Cochrane pairwise meta-analyses using a six-criterion actionability framework. It recomputes each meta-analysis, applies significance, prediction interval, robustness, audit, volume, and publication-bias checks, then exports verdict tables and a dashboard-ready summary.

## Inputs

- `C:\Users\user\OneDrive - NHS\Documents\Pairwise70\data`
- `C:\MetaAudit\results\audit_results.csv`
- `C:\FragilityAtlas\data\output\fragility_atlas_results.csv`

## Repository Layout

- `compute_verdicts.py`: verdict engine
- `build_dashboard.py`: embeds exported results into `dashboard.html`
- `results/verdicts.csv`: MA-level verdict output
- `results/summary.json`: aggregate summary and waterfall counts
- `dashboard.html`: interactive dashboard artifact
- `paper/manuscript.md`: manuscript draft
- `tests/test_verdicts.py`: test suite

## Run

```powershell
python compute_verdicts.py
python compute_verdicts.py --max-reviews 100
python build_dashboard.py
```

## Validate

```powershell
python -m pytest -q
```

## Current Outputs

- `results/verdicts.csv` contains one row per meta-analysis with verdict and failed criteria
- `results/summary.json` contains actionable counts, failure rates, and the sequential waterfall
- `dashboard.html` is generated from the current contents of `results/`

## Notes

- The dashboard depends on `results/verdicts.csv` and `results/summary.json`, so rerun `build_dashboard.py` after refreshing the verdict exports.
- Reviews not covered by FragilityAtlas receive the existing benefit-of-doubt behavior implemented in `compute_verdicts.py`.
