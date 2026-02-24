# Model Card: GP-Based Weekly Black-Box Query Proposer

## Overview

**Model name:** GP + Expected Improvement Weekly Proposer  
**Model family:** Sequential surrogate-based black-box optimisation helper  
**Primary implementation:** `black_box_optimizer.py`  
**Execution entry point:** `notebooks/bboWeeklyRunner.ipynb`

This model card documents the optimiser implementation currently present in this repository. The active code uses a **Gaussian Process (GP)** surrogate with **Expected Improvement (EI)** acquisition and random candidate search.

The system is designed to suggest the next query point from existing input-output observations. In the current code path, the optimiser proposes `x_next` values but does not call the external black-box service internally.

## Intended Use

This implementation is intended for:

- Sequential optimisation where function internals are unknown.
- Small-data settings with expensive evaluations.
- Continuous domains bounded to `[0, 1]`.
- Weekly proposal generation workflows (one proposal per function per round).

Typical use context in this repository:

- 8 independent functions (2D to 8D).
- Historical records stored under `queries/week*/`.
- Starter observations stored under `data/initial_data/`.

## Not Intended For

This implementation is not designed for:

- Discrete/combinatorial search spaces.
- High-throughput optimisation requiring strong parallelism.
- Formal global-optimum guarantees.
- End-to-end autonomous optimisation without externally provided outputs.

## Model Details

### Surrogate Model

- `GaussianProcessRegressor` from scikit-learn
- Kernel: Matérn (`nu=2.5`)
- Settings: `alpha=1e-6`, `normalize_y=True`

### Acquisition Function

- Expected Improvement (EI) with exploration term `xi=0.01`
- Candidate scoring uses GP predictive mean and standard deviation

### Candidate Search

- Samples random candidates uniformly in `[0, 1]^d`
- Default candidate pool size: `5000`
- Returns candidate with highest EI
- Final point is clipped to `[0, 1]` and rounded to 6 decimals

## Input / Output Interface

### Inputs

- `initial_inputs`: array of shape `(n_samples, n_features)`
- `initial_outputs`: array of shape `(n_samples,)`
- `max_queries`: number of proposal iterations to run
- `seed`: RNG seed for reproducibility

### Outputs

- Returns `(inputs, outputs)` arrays
- Current implementation returns copied arrays (no internal black-box evaluation)
- Prints proposed `x_next` per iteration

## Repository Integration

- Weekly text files live in `queries/week1` ... `queries/week13`
- Notebook `notebooks/bboWeeklyRunner.ipynb` loads weekly files and calls `optimise_black_box(...)`
- Initial `.npy` starter data is in `data/initial_data/function_*/`

## Assumptions

- Objective behaves sufficiently smoothly for GP surrogate modelling to be useful.
- Existing observations contain enough signal to support local EI ranking.
- Input domain is continuous and bounded.

## Limitations

- No direct objective evaluation inside `optimise_black_box`.
- No automatic append of newly observed outputs within this implementation.
- EI optimisation via random search can miss better points in higher dimensions.
- Fixed GP settings may not be optimal for every function.

## Evaluation Context

Intended evaluation is across the 8 capstone functions with sequential weekly updates. Practical indicators include:

- Quality of proposed points over rounds
- Improvement in best observed value after external evaluation
- Stability of proposal behaviour as dataset grows

Formal regret bounds are not implemented in this repository.

## Transparency and Reproducibility

- The model logic is fully visible in `black_box_optimizer.py`.
- Weekly run process is documented and executable through the notebook runner.
- Data artefacts are stored in explicit week-based folders for traceability.

## Future Extension Path

Potential upgrades, if needed:

- Add callback support for external objective evaluation and in-loop appending.
- Introduce adaptive `xi` schedules and candidate budget scaling.
- Add multi-start or gradient-based acquisition maximisation.
- Benchmark against alternative surrogates or hybrid GP–NN strategies.
