# sentinel:skip-file — hardcoded paths are fixture/registry/audit-narrative data for this repo's research workflow, not portable application configuration. Same pattern as push_all_repos.py and E156 workbook files.
"""ActionableEvidence — compute GO/NO-GO verdicts for 6,229 Cochrane meta-analyses.

For each MA, evaluates 6 independent criteria. ALL must pass for ACTIONABLE.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import sys
import time
from pathlib import Path

# MetaAudit imports
sys.path.insert(0, "C:/MetaAudit")
from metaaudit.loader import load_all_reviews, DataType  # noqa: E402
from metaaudit.recompute import recompute_ma  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

# ── Paths ──────────────────────────────────────────────────────────────
PAIRWISE70_DIR = Path("C:/Users/user/OneDrive - NHS/Documents/Pairwise70/data")
AUDIT_RESULTS = Path("C:/MetaAudit/results/audit_results.csv")
FRAGILITY_RESULTS = Path("C:/FragilityAtlas/data/output/fragility_atlas_results.csv")
OUTPUT_DIR = Path("C:/Models/ActionableEvidence/results")

# ── Thresholds ─────────────────────────────────────────────────────────
SIGNIFICANCE_ALPHA = 0.05
PI_NULL = 0.0  # log-scale null for ratios and differences
MIN_K = 5
MIN_N = 500
EGGER_THRESHOLD = 0.10
MIN_K_EGGER = 10

# ── Seed ───────────────────────────────────────────────────────────────
np.random.seed(42)


def extract_review_id(ma_id: str) -> str:
    """Extract CD number from ma_id like 'CD000028_pub4_data__A1'."""
    m = re.match(r"(CD\d+)", ma_id)
    return m.group(1) if m else ""


def compute_total_n(df: pd.DataFrame) -> int:
    """Compute total participants from study-level data."""
    total = 0
    if "Experimental.N" in df.columns:
        total += df["Experimental.N"].dropna().sum()
    if "Control.N" in df.columns:
        total += df["Control.N"].dropna().sum()
    return int(total)


def load_audit_data() -> dict:
    """Load MetaAudit results. Returns dict keyed by ma_id.

    For each ma_id:
      - n_fails: count of FAIL or CRITICAL severity rows
      - pub_bias_fail: whether pub_bias module has FAIL or CRITICAL
    """
    print("Loading MetaAudit audit results...")
    df = pd.read_csv(AUDIT_RESULTS)
    result = {}
    for ma_id, group in df.groupby("ma_id"):
        fails = group[group["severity"].isin(["FAIL", "CRITICAL"])]
        n_fails = len(fails)
        pub_bias_rows = group[group["module"] == "pub_bias"]
        pub_bias_fail = any(pub_bias_rows["severity"].isin(["FAIL", "CRITICAL"]))
        result[ma_id] = {
            "n_fails": n_fails,
            "pub_bias_fail": pub_bias_fail,
        }
    print(f"  Loaded audit data for {len(result)} MAs")
    return result


def load_fragility_data() -> dict:
    """Load FragilityAtlas results. Returns dict keyed by review_id (CD number).

    classification: Robust, Moderate, Fragile, Unstable
    """
    print("Loading FragilityAtlas results...")
    df = pd.read_csv(FRAGILITY_RESULTS)
    result = {}
    for _, row in df.iterrows():
        result[row["review_id"]] = row["classification"]
    print(f"  Loaded fragility data for {len(result)} reviews")
    return result


def pi_crosses_null(pi_lower: float, pi_upper: float, measure: str) -> bool:
    """Check if prediction interval crosses the null value.

    For log-scale measures (logOR, logRR, logHR), null = 0.
    For MD/SMD/GIV, null = 0.
    """
    null = PI_NULL  # 0 on log-scale or raw scale
    return pi_lower <= null <= pi_upper


def evaluate_criteria(
    recomp,
    total_n: int,
    audit_info: dict | None,
    fragility_class: str | None,
    fragility_covered: bool,
) -> dict:
    """Evaluate all 6 criteria for one MA. Returns dict with pass/fail for each."""

    # 1. Statistical significance (HKSJ p < 0.05)
    c1_significant = recomp.significant and recomp.p_value < SIGNIFICANCE_ALPHA

    # 2. Prediction interval concordance (PI does not cross null)
    if not recomp.pi_computable:
        # k < 3: PI not computable, pass by default
        c2_pi_ok = True
    else:
        c2_pi_ok = not pi_crosses_null(recomp.pi_lower, recomp.pi_upper, recomp.measure)

    # 3. Multiverse robustness (Robust or Moderate)
    if not fragility_covered:
        # Review not in FragilityAtlas: benefit of doubt = pass
        c3_robust = True
    else:
        c3_robust = fragility_class in ("Robust", "Moderate")

    # 4. Low audit flag burden (0 FAIL/CRITICAL flags)
    if audit_info is None:
        # No audit data: cannot verify, treat as fail
        c4_no_fails = False
    else:
        c4_no_fails = audit_info["n_fails"] == 0

    # 5. Sufficient evidence volume (k >= 5 AND total N >= 500)
    c5_volume = recomp.k >= MIN_K and total_n >= MIN_N

    # 6. No publication bias signal
    # Egger's test only meaningful for k >= 10; if k < 10 pass by default
    if recomp.k < MIN_K_EGGER:
        c6_no_pub_bias = True
    elif audit_info is None:
        c6_no_pub_bias = False
    else:
        # pub_bias module FAIL/CRITICAL means bias detected
        c6_no_pub_bias = not audit_info["pub_bias_fail"]

    # Build failed criteria list
    failed = []
    if not c1_significant:
        failed.append("significance")
    if not c2_pi_ok:
        failed.append("prediction_interval")
    if not c3_robust:
        failed.append("robustness")
    if not c4_no_fails:
        failed.append("audit_flags")
    if not c5_volume:
        failed.append("evidence_volume")
    if not c6_no_pub_bias:
        failed.append("pub_bias")

    verdict = "ACTIONABLE" if len(failed) == 0 else "NOT YET"

    return {
        "significant": c1_significant,
        "pi_ok": c2_pi_ok,
        "robust": c3_robust,
        "no_fails": c4_no_fails,
        "volume_ok": c5_volume,
        "no_pub_bias": c6_no_pub_bias,
        "verdict": verdict,
        "failed_criteria": failed,
    }


def run_pipeline(max_reviews: int | None = None) -> None:
    """Run the full ActionableEvidence pipeline."""
    t0 = time.time()

    # Load auxiliary data
    audit_data = load_audit_data()
    fragility_data = load_fragility_data()

    # Load Pairwise70
    print(f"Loading Pairwise70 from {PAIRWISE70_DIR}...")
    reviews = load_all_reviews(str(PAIRWISE70_DIR), max_reviews=max_reviews)
    total_analyses = sum(len(r.analyses) for r in reviews)
    print(f"  Loaded {len(reviews)} reviews with {total_analyses} MAs")

    # Process each MA
    verdicts = []
    n_processed = 0
    criteria_pass_counts = {
        "significance": 0,
        "prediction_interval": 0,
        "robustness": 0,
        "audit_flags": 0,
        "evidence_volume": 0,
        "pub_bias": 0,
    }
    criteria_fail_counts = {k: 0 for k in criteria_pass_counts}
    fragility_not_covered_count = 0

    for review in reviews:
        review_id = extract_review_id(review.review_id)
        fragility_class = fragility_data.get(review_id)
        fragility_covered = fragility_class is not None

        for ag in review.analyses:
            ma_id = ag.ma_id
            total_n = compute_total_n(ag.df)

            # Recompute pooled effect
            try:
                recomp = recompute_ma(ag.df, ag.data_type)
            except Exception as e:
                print(f"  ERROR recomputing {ma_id}: {e}")
                continue

            # Get audit info
            audit_info = audit_data.get(ma_id)

            # Evaluate criteria
            result = evaluate_criteria(
                recomp, total_n, audit_info, fragility_class, fragility_covered
            )

            # Track counts
            for crit in criteria_pass_counts:
                key_map = {
                    "significance": "significant",
                    "prediction_interval": "pi_ok",
                    "robustness": "robust",
                    "audit_flags": "no_fails",
                    "evidence_volume": "volume_ok",
                    "pub_bias": "no_pub_bias",
                }
                if result[key_map[crit]]:
                    criteria_pass_counts[crit] += 1
                else:
                    criteria_fail_counts[crit] += 1

            if not fragility_covered:
                fragility_not_covered_count += 1

            verdicts.append({
                "ma_id": ma_id,
                "review_id": review_id,
                "k": recomp.k,
                "total_n": total_n,
                "estimate": round(recomp.estimate, 6) if math.isfinite(recomp.estimate) else None,
                "p_value": round(recomp.p_value, 6) if math.isfinite(recomp.p_value) else None,
                "significant": result["significant"],
                "pi_crosses_null": not result["pi_ok"],
                "robustness": fragility_class if fragility_covered else "not_covered",
                "n_audit_fails": audit_info["n_fails"] if audit_info else None,
                "has_pub_bias": not result["no_pub_bias"],
                "verdict": result["verdict"],
                "failed_criteria": ";".join(result["failed_criteria"]) if result["failed_criteria"] else "",
            })

            n_processed += 1
            if n_processed % 100 == 0:
                elapsed = time.time() - t0
                print(f"  Processed {n_processed}/{total_analyses} MAs ({elapsed:.1f}s)")

    elapsed = time.time() - t0
    print(f"\nProcessed {n_processed} MAs in {elapsed:.1f}s")

    # ── Write verdicts.csv ─────────────────────────────────────────────
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUTPUT_DIR / "verdicts.csv"
    fieldnames = [
        "ma_id", "review_id", "k", "total_n", "estimate", "p_value",
        "significant", "pi_crosses_null", "robustness", "n_audit_fails",
        "has_pub_bias", "verdict", "failed_criteria",
    ]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(verdicts)
    print(f"Wrote {csv_path} ({len(verdicts)} rows)")

    # ── Compute summary ────────────────────────────────────────────────
    n_actionable = sum(1 for v in verdicts if v["verdict"] == "ACTIONABLE")
    n_not_yet = sum(1 for v in verdicts if v["verdict"] == "NOT YET")
    total = len(verdicts)
    pct_actionable = round(100.0 * n_actionable / total, 1) if total > 0 else 0.0

    criteria_failure_rates = {}
    for crit in criteria_fail_counts:
        rate = round(100.0 * criteria_fail_counts[crit] / total, 1) if total > 0 else 0.0
        criteria_failure_rates[crit] = rate

    # Find most common single failure (MAs that fail on exactly 1 criterion)
    single_failures = {}
    for v in verdicts:
        fc = v["failed_criteria"]
        if fc and ";" not in fc:
            single_failures[fc] = single_failures.get(fc, 0) + 1
    most_common_single = max(single_failures, key=single_failures.get) if single_failures else "none"

    # Reviews with any actionable MA
    reviews_with_actionable = set()
    reviews_all_actionable = {}
    for v in verdicts:
        rid = v["review_id"]
        if v["verdict"] == "ACTIONABLE":
            reviews_with_actionable.add(rid)
        if rid not in reviews_all_actionable:
            reviews_all_actionable[rid] = True
        if v["verdict"] != "ACTIONABLE":
            reviews_all_actionable[rid] = False
    n_reviews_all_actionable = sum(1 for v in reviews_all_actionable.values() if v)

    # Waterfall: starting from total, how many survive each successive filter
    # Apply filters in order: significance -> PI -> robustness -> audit -> volume -> pub_bias
    waterfall = {"total": total}
    surviving = set(range(total))
    filter_order = [
        ("significance", "significant"),
        ("prediction_interval", "pi_crosses_null"),
        ("robustness", "robustness"),
        ("audit_flags", "n_audit_fails"),
        ("evidence_volume", "volume_ok"),
        ("pub_bias", "has_pub_bias"),
    ]

    for crit_name, _ in filter_order:
        key_map = {
            "significance": lambda v: v["significant"],
            "prediction_interval": lambda v: not v["pi_crosses_null"],
            "robustness": lambda v: v["robustness"] in ("Robust", "Moderate", "not_covered"),
            "audit_flags": lambda v: v["n_audit_fails"] is not None and v["n_audit_fails"] == 0,
            "evidence_volume": lambda v: v["k"] >= MIN_K and v["total_n"] >= MIN_N,
            "pub_bias": lambda v: not v["has_pub_bias"],
        }
        new_surviving = set()
        for i in surviving:
            if key_map[crit_name](verdicts[i]):
                new_surviving.add(i)
        surviving = new_surviving
        waterfall[f"after_{crit_name}"] = len(surviving)

    summary = {
        "total_mas": total,
        "actionable": n_actionable,
        "actionable_pct": pct_actionable,
        "not_yet": n_not_yet,
        "criteria_failure_rates": criteria_failure_rates,
        "most_common_single_failure": most_common_single,
        "single_failure_counts": single_failures,
        "reviews_with_any_actionable": len(reviews_with_actionable),
        "reviews_all_actionable": n_reviews_all_actionable,
        "fragility_not_covered": fragility_not_covered_count,
        "waterfall": waterfall,
        "elapsed_seconds": round(elapsed, 1),
    }

    json_path = OUTPUT_DIR / "summary.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote {json_path}")

    # ── Print summary ──────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("ACTIONABLE EVIDENCE — FINAL SUMMARY")
    print("=" * 70)
    print(f"Total MAs analyzed:         {total}")
    print(f"ACTIONABLE:                 {n_actionable} ({pct_actionable}%)")
    print(f"NOT YET:                    {n_not_yet}")
    print(f"Reviews with any ACTIONABLE: {len(reviews_with_actionable)}")
    print(f"Reviews ALL ACTIONABLE:      {n_reviews_all_actionable}")
    print(f"FragilityAtlas not covered:  {fragility_not_covered_count} MAs")
    print()
    print("Criteria failure rates:")
    for crit, rate in sorted(criteria_failure_rates.items(), key=lambda x: -x[1]):
        print(f"  {crit:25s} {rate:5.1f}%  ({criteria_fail_counts[crit]} MAs)")
    print()
    print(f"Most common single failure: {most_common_single}")
    print()
    print("Waterfall (sequential filtering):")
    prev = total
    for key, val in waterfall.items():
        label = key.replace("after_", "+ ").replace("_", " ")
        drop = prev - val if key != "total" else 0
        print(f"  {label:30s} {val:6d}  (-{drop})" if key != "total" else f"  {'total':30s} {val:6d}")
        prev = val
    print()
    print(f"Pipeline completed in {elapsed:.1f}s")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="ActionableEvidence verdict engine")
    parser.add_argument("--max-reviews", type=int, default=None,
                        help="Limit to N reviews (for development)")
    args = parser.parse_args()
    run_pipeline(max_reviews=args.max_reviews)


if __name__ == "__main__":
    main()
