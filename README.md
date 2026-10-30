# NSL-KDD Direct Comparison — Research Package

Replication-oriented comparison of an out-of-fold **stacking** ensemble against the SVM,
Logistic Regression and KNN baselines of Vibhute et al. (2024, *Procedia Computer Science* 233,
960–969, [doi:10.1016/j.procs.2024.03.285](https://doi.org/10.1016/j.procs.2024.03.285)) on
binary NSL-KDD (normal = 0, attack = 1). All methods are evaluated on the **same saved
evaluation rows**, so differences are paired.

> This is **not** an exact replication of the reported 98.24 % accuracy: the authors' split
> indices and exact feature list are not available. Assumptions are recorded in
> `paper_reconstruction.json`.

## Design

| Item | Setting |
|---|---|
| Protocols | `paper70` (70/30), `paper75` (75/25), `official` (KDDTrain+ → KDDTest+) |
| Feature arms | `rf_threshold_encoded`, `rf_top9_group`, `all` (41 features) |
| Seeds | 42, 52, 62, 72, 82 |
| Primary metric | accuracy; also precision/recall/F1 (attack), Macro-F1, MCC, ROC-AUC, PR-AUC, FPR |
| Inference | paired accuracy deltas, exact McNemar per seed (Holm, exploratory), grouped bootstrap |
| Engine | `nslkdd-direct-v2`, profile `journal` |

## Headline result (STACK vs. re-run KNN, `rf_top9_group`, 5 seeds)

| Protocol | Mean Δ accuracy (pp) | Seeds positive |
|---|---|---|
| paper70 | +1.18 | 5/5 |
| paper75 | +1.11 | 5/5 |
| official | −1.56 | 0/5 |

Full numbers: `summary_mean_std.csv`, `paired_accuracy_summary.csv`, `paired_accuracy_by_seed.csv`.

## Repository contents

| Path | Content |
|---|---|
| `NSLKDD_Direct_Comparison_Colab (1).ipynb` | Complete experiment code (Colab/Jupyter) |
| `direct_protocol_lock.json` | Locked configuration, algorithm signature, software versions |
| `experiment_metadata.json` | Run status, Python/platform, package versions, dataset audit |
| `dataset_audit.json` | Row counts, SHA-256, duplicates, conflicts, train/test overlap |
| `paper_reconstruction.json` | What was reconstructed from the paper and what was assumed |
| `paper_historical_reference.csv` | Reported paper values (kept separate from our results) |
| `splits/<protocol>/seed*.csv` | Train/evaluation row assignments for every protocol and seed |
| `suites/<protocol>/seed*/<arm>/` | Predictions (`predictions.npz`), OOF probabilities (`oof.npz`, `oof_folds.csv`), selected features, metrics, warnings |
| `metrics_by_seed.csv`, `summary_mean_std.csv` | Metrics per seed and aggregated |
| `paired_accuracy_*.csv`, `interpretation.json` | Paired comparisons and audit messages |
| `figures/` | Accuracy and paired-delta figures |
| `data/` | Dataset provenance and checksums (raw data not redistributed) |
| `scripts/fetch_nsl_kdd.py` | Download from the frozen mirror and verify SHA-256 and row counts |

## Data provenance

NSL-KDD (Canadian Institute for Cybersecurity, UNB, 2009) is **not redistributed**. The official
page (https://www.unb.ca/cic/datasets/nsl.html) no longer serves the files; the experiment uses an
unofficial mirror frozen at commit `27bbbdf5c5cccf9970b8b6037a0f19dc09c5a0a9`
(https://github.com/Jehuty4949/NSL_KDD).

| File | Rows | SHA-256 |
|---|---|---|
| `KDDTrain+.txt` | 125,973 | `1b86d2f957b33082081bba410fe129b475efebcc13c9014c3f447c8271aadf95` |
| `KDDTest+.txt` | 22,544 | `fa46b0935342616aa83b7c2578db355b6a7aaabbc492248172c7a1e8b7ab8f84` |

## Reproduce

```bash
pip install -r requirements.txt          # Python 3.13; versions as recorded in experiment_metadata.json
python scripts/fetch_nsl_kdd.py data     # downloads and verifies both files
NSL_DATA_DIR=data NSL_OUT_DIR=rerun jupyter nbconvert --to notebook --execute "NSLKDD_Direct_Comparison_Colab (1).ipynb"
```

On Colab, open the notebook and run all cells; data are downloaded and verified automatically.
The last two notebook cells only zip and download outputs in Colab and can be skipped elsewhere.

## Citation

See `CITATION.cff`. Please also cite NSL-KDD: M. Tavallaee, E. Bagheri, W. Lu, A. A. Ghorbani,
"A Detailed Analysis of the KDD CUP 99 Data Set," CISDA 2009,
[doi:10.1109/CISDA.2009.5356528](https://doi.org/10.1109/CISDA.2009.5356528).

## Licence

Code: MIT (`LICENSE`). Results and derived data: CC BY 4.0 (`LICENSE-DATA.md`).
