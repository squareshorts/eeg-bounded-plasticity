# Bounded residual plasticity in adaptive motor-imagery EEG decoding

This repository packages the numerical results, configuration records, and figures associated with **“Bounded residual plasticity reduces negative transfer in adaptive motor-imagery EEG decoding”** (manuscript under preparation for journal submission).

The experimental question is whether constraining subject-specific adaptation to a low-rank latent residual reduces participant-level negative transfer. The adaptation rule keeps the source encoder and classifier fixed and bounds source-probe latent displacement to 2% for the selected rank-2 residual.

## Reported evaluation

- **PhysioNet EEG Motor Movement/Imagery Database:** development on R04 → R08/R12; task-level evaluation on R06 → R10/R14 in the same 109-person cohort. Evaluation tasks differ, but the participants overlap with development.
- **BCI Competition IV-2a:** AxxT → AxxE, nine participants, with the same adaptation configuration and separately fitted four-class source model. The BCI dataset had prior exploratory use, as disclosed in the manuscript.
- **Cohort-stratified combined analysis:** 118 participants (109 PhysioNet + 9 BCI-IV-2a). Negative transfer means a loss **strictly greater than one percentage point** in balanced accuracy in any designated future evaluation session. The reported event counts were 33/118 for unconstrained full-encoder updates, 25/118 for hard-KL adaptation, and 5/118 for bounded residual adaptation. Mean bounded residual utility was −0.042 percentage points.
- **Supplementary raw-EEG check:** an EEGNet-style representation evaluated on 109 PhysioNet participants, excluded from the 118-person combined analysis. Its negative-transfer counts were 22/109 for unrestricted encoder adaptation and 5/109 for bounded residual adaptation.

## Contents

- `data/cohort_stratified_recheck.json` — archived primary combined-analysis statistical summary, paired contingency tables, bootstrap and inferential results.
- `data/eegnet_architecture_robustness_results.csv` — 436 raw-EEG method-by-participant output rows, including future-session utilities.
- `data/eegnet_architecture_robustness_summary.json`, `data/eegnet_frozen_recipe.json`, `data/eegnet_no_leakage_audit.json`, and `data/parameter_update_summary.json` — configuration and frozen-run provenance records.
- `figures/` — archived illustrations and provenance description; `scripts/make_architecture_diagram.py` regenerates the architecture illustration.
- `scripts/verify_results.py` — standard-library numerical checks using the released primary summary and raw-EEG participant rows.
- `RELEASE_NOTES_v1.0.0.md` — proposed release description for Zenodo-linked GitHub publication.

Run the numerical checker from the repository root:

```sh
python scripts/verify_results.py
```

## Reproducibility boundary

**This is a numerical-results and verification archive, not a complete end-to-end model-training release.** The original preprocessing, encoder training, feature extraction and adaptation scripts, the PhysioNet/BCI-IV-2a participant-level files underpinning the primary 118-person analysis, and source model checkpoints were not present in the supplied audited manuscript ZIP and have not been reconstructed here. The verifier recomputes exact paired p-values from the archived primary contingency tables, and independently recomputes the supplementary raw-EEG negative-transfer events from its 436 output rows. It does not refit EEG models or regenerate the primary model predictions.

The original project assets must be recovered from the researcher's local workspace and source hashes checked before this archive can be described as fully reproducible. **Do not claim complete code availability or training-level reproducibility on the basis of this package alone.**

The original JSON records included machine-specific Windows paths. Their public copies omit those path-bearing fields; numerical outputs, method settings, and checksums are preserved. In-place source data and training scripts were not altered by the public export.

## Dataset origins

- PhysioNet EEG Motor Movement/Imagery Database: https://physionet.org/content/eegmmidb/1.0.0/
- BCI Competition IV-2a: https://www.bbci.de/competition/iv/

These source EEG recordings are **not redistributed**. Obtain them from their original publishers under the applicable dataset terms and cite the source datasets in downstream publications.

## Publication and citing

This repository does not contain the manuscript's LaTeX source. A definitive author list and archival DOI should be added to release metadata once confirmed. Cite the research article after acceptance and the Zenodo DOI assigned to the final deposited release.

## Code and records rights

The newly written `scripts/verify_results.py` is provided under the MIT license in `LICENSE-VERIFY-CODE.txt`. Reuse of research outputs and any other scripts must respect the authors' rights and the upstream dataset terms. No licence is asserted here on behalf of third-party data providers.
