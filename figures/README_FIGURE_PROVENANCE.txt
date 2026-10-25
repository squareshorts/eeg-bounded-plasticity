FIGURE PROVENANCE

bounded_residual_architecture.pdf
  Reconstructed directly from the architecture specified in main.tex: frozen source encoder/classifier, rank-2 residual U GELU(Vz), and deterministic 2% source-probe latent-displacement projection.

cross_dataset_negative_transfer.png
  Replotted from the reported frozen event counts:
  - held-out PhysioNet R06/R10/R14: 31/109 unconstrained, 25/109 hard-KL, 5/109 bounded residual;
  - BCI-IV-2a: 2/9 unconstrained, 0/9 hard-KL, 0/9 bounded residual.

cross_dataset_safety_utility_points.png
  Replotted from reported harm rates and mean utilities for PhysioNet development, held-out PhysioNet evaluation, and BCI-IV-2a.

safety_utility_frontier.png
  Replotted from PhysioNet development statistics: unconstrained 21.10% / -0.141 pp; hard-KL 17.43% / +0.072 pp; bounded residual 3.67% / +0.156 pp.

No participant-level BCI-IV-2a utility plot was fabricated; see README_OVERLEAF.txt.
