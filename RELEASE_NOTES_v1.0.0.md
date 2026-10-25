# v1.0.0 — Bounded residual plasticity: numerical results and verification archive

**Associated manuscript:** *Bounded residual plasticity reduces negative transfer in adaptive motor-imagery EEG decoding*.

This release archives the numerical analyses, configuration records and figure artifacts used to evaluate the safety–utility trade-off of bounded residual adaptation in motor-imagery EEG decoding. The architecture retains the source encoder and classifier and confines participant-specific updates to a rank-2 residual with a 2% source-probe displacement bound.

**Main findings.** The cohort-stratified combined analysis consists of 109 PhysioNet participants evaluated on held-out tasks and nine BCI Competition IV-2a participants evaluated cross-dataset. Negative transfer exceeding one percentage point in at least one later evaluation session occurred in 5/118 participants under bounded residual adaptation, compared with 33/118 under unconstrained encoder adaptation and 25/118 under hard-KL adaptation. Mean bounded residual utility was −0.042 percentage points. An additional EEGNet-style raw-EEG robustness analysis (109 PhysioNet participants, outside the combined cohort analysis) found 5/109 negative-transfer events for bounded adaptation compared with 22/109 for unconstrained adaptation.

**Included records.** Cohort-stratified statistical recheck, paired comparison tables, bootstrap summaries, raw-EEG participant-by-method outputs (436 rows), frozen configuration and no-leakage audit records, parameter-update audit summaries, figures and a Python numerical verification script. Run `python scripts/verify_results.py` for the independent checks supported by the released records.

**Scope of reproducibility.** The available package supports independent verification of numerical summaries and recomputation of the supplementary raw-EEG event counts. It does not contain the original EEG preprocessing and training pipelines, primary participant-level output files or model checkpoints. Full end-to-end retraining cannot be reproduced from this archive. These limitations must remain visible until the original project code and primary data-derived files are added and validated.

PhysioNet EEG Motor Movement/Imagery Database and BCI Competition IV-2a EEG source archives remain available from their respective providers and are not included.

**Release provenance:** assembled from the audited pre-submission package dated 25 October 2026. Source-file checksums are distributed in `SHA256SUMS.txt`. No publication DOI is assigned in this draft; Zenodo metadata should use the confirmed author names and order.
