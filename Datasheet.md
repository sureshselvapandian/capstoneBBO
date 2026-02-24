# Datasheet for the Black-Box Optimisation (BBO) Capstone Dataset

## Motivation

This dataset supports a sequential black-box optimisation workflow where objective functions are unknown and evaluations are limited. The main goal is to study how query choices improve outcomes when each new observation is expensive and must be selected under uncertainty.

It is particularly useful for analysing exploration/exploitation trade-offs, low-data surrogate behaviour, and weekly strategy updates in constrained optimisation settings.

## Composition

The repository dataset contains observations for 8 independent black-box functions. Each function is treated as a separate optimisation problem.

### Inputs

Inputs are continuous vectors with dimensionality from 2 to 8 depending on function index. Values are bounded in `[0, 1]` and are typically represented with up to 6 decimal places.

### Outputs

Each input maps to one scalar output. All tasks are framed as maximisation, so higher output values indicate better performance.

## Dataset Size and Round Structure

The dataset is intentionally sparse. For each function, optimisation starts from provided initial observations and then evolves through weekly additions (week1 through week13 in this repository). This design mirrors expensive-evaluation scenarios where each added query matters.

## Data Organisation and Location

Data in this repository is split across two locations:

1. `data/initial_data/`
	 - `function_1/` ... `function_8/`
	 - each contains:
		 - `initial_inputs.npy`
		 - `initial_outputs.npy`

2. `queries/week1/` ... `queries/week13/`
	 - per-function text records:
		 - `function_1_inputs.txt` ... `function_8_inputs.txt`
		 - `function_1_outputs.txt` ... `function_8_outputs.txt`
	 - aggregate files (when present):
		 - `inputs.txt`
		 - `outputs.txt`

This structure preserves both the starter state (`.npy`) and the week-by-week working records (`.txt`).

## Gaps and Limitations

Sampling density is non-uniform by design. Some regions receive dense local refinement while other areas remain lightly explored, especially for higher-dimensional functions.

No confirmed global optimum is provided. Performance is therefore assessed through observed improvement over rounds rather than guaranteed optimality.

## Collection Process

Data collection follows a sequential weekly protocol:

- Begin from provided initial observations.
- Propose one new query per function per round.
- Receive external evaluation outputs.
- Update the next week’s records.

In the current repository implementation, query proposals are generated with a GP + Expected Improvement approach in `black_box_optimizer.py`, and weekly orchestration is handled by `notebooks/bboWeeklyRunner.ipynb`.

## Preprocessing

The repository stores raw values in `.npy` and `.txt` formats. Parsing/conversion happens during execution (for example, converting array-like text in weekly files into NumPy arrays). Any additional scaling is strategy-dependent and should be applied using only information available up to the current round.

## Intended Uses

This dataset is intended for research and educational work on sequential black-box optimisation under data scarcity. Typical uses include:

- Evaluating GP-based proposal strategies.
- Comparing weekly query policies under strict budgets.
- Teaching iterative optimisation reasoning and diagnostics.

## Inappropriate Uses

This dataset is not suitable for large i.i.d. supervised-learning benchmarks or broad generalisation claims.

Because the functions are synthetic/abstract, it is not appropriate for fairness, demographic, or societal impact analysis.

## Distribution and Maintenance

The dataset is distributed with this repository alongside the optimisation code and documentation. Maintenance is performed in-repo by updating week folders and associated docs. Any naming/format updates (for example, file renaming or txt-to-npy conversion scripts) are tracked as project files for reproducibility.
