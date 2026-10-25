#!/usr/bin/env python3
"""Check released numerical summaries and the raw-EEG participant results.

Standard library only. Checks stored primary paired tables and independently
recomputes raw-EEG events from participant rows. Does not train an EEG model.
"""
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def exact_mcnemar(comparator_only, residual_only):
    n = comparator_only + residual_only
    if not n:
        return 1.0
    k = min(comparator_only, residual_only)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2**n)


def near(a, b, tol=1e-10):
    assert math.isclose(a, b, rel_tol=tol, abs_tol=tol), (a, b)


def main():
    with (DATA / "cohort_stratified_recheck.json").open(encoding="utf-8") as f:
        primary = json.load(f)
    with (DATA / "eegnet_architecture_robustness_summary.json").open(encoding="utf-8") as f:
        raw_summary = json.load(f)

    n = primary["cohort_results"]["combined"]["n_participants"]
    assert n == 118
    combined = primary["cohort_results"]["combined"]["methods"]
    expected = {"unconstrained": 33, "hard_kl": 25, "residual": 5}
    for method, count in expected.items():
        assert combined[method]["harm_gt_1pp_n"] == count
        near(combined[method]["harm_gt_1pp_rate"], count / n)
    near(combined["residual"]["mean_utility_percentage_points"], -0.04203658864675804)
    for compare in ["residual_vs_unconstrained", "residual_vs_hard_kl"]:
        entry = primary["paired_mcnemar"][compare]
        a = entry["prevented"]
        b = entry["introduced"]
        assert a + b == entry["discordant"]
        assert sum(entry["two_by_two"].values()) == n
        near(exact_mcnemar(a, b), entry["p_exact_two_sided"])
        print(f"Primary {compare}: {a} prevented, {b} introduced; p={exact_mcnemar(a,b):.12g}")

    by_id = defaultdict(dict)
    with (DATA / "eegnet_architecture_robustness_results.csv").open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 436
    methods = {"static", "unconstrained", "hard_kl", "bounded_residual"}
    for row in rows:
        pid = int(row["participant_id"])
        method = row["method"]
        assert 1 <= pid <= 109
        assert method in methods and method not in by_id[pid]
        by_id[pid][method] = row
    assert len(by_id) == 109
    assert all(set(record) == methods for record in by_id.values())

    def harmed(row):
        utility = min(float(row["utility_r10"]), float(row["utility_r14"]))
        flag = row["negative_transfer_gt_1pp"].lower() == "true"
        assert flag == (utility < -0.01)
        return flag

    counts = {}
    mean_ba = {}
    mean_utility = {}
    for method in sorted(methods):
        rs = [record[method] for record in by_id.values()]
        counts[method] = sum(harmed(row) for row in rs)
        mean_ba[method] = sum(float(row["mean_r10_r14_ba"]) for row in rs)/109
        mean_utility[method] = sum(float(row["mean_utility_relative_to_static"]) for row in rs)/109
        print(f"Raw-EEG {method}: harmful={counts[method]}/109, BA={mean_ba[method]*100:.6f}%, utility={mean_utility[method]*100:+.6f} pp")

    assert counts == {"static":0,"unconstrained":22,"hard_kl":16,"bounded_residual":5}
    near(mean_ba["static"]*100, 57.22012887723897, tol=1e-6)
    assert raw_summary["n_subjects"] == 109
    compared = [record for record in by_id.values()]
    prevented = sum(harmed(record["unconstrained"]) and not harmed(record["bounded_residual"]) for record in compared)
    introduced = sum(harmed(record["bounded_residual"]) and not harmed(record["unconstrained"]) for record in compared)
    assert (prevented, introduced) == (21, 4)
    near(exact_mcnemar(prevented,introduced),0.0009105205535888672)
    print(f"Raw-EEG bounded vs unconstrained: prevented={prevented}, introduced={introduced}; exact paired p={exact_mcnemar(prevented,introduced):.12g}")
    print("PASS: archival primary paired-table and raw-EEG participant-level checks")

if __name__ == "__main__":
    main()
