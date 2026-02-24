# Methodology: Repository-Aligned Weekly Optimisation Workflow

## Scope and Objective

This project implements a sequential black-box optimisation workflow over 8 independent functions. The goal each week is to choose one high-quality query per function based on observed history, then update records after receiving the external evaluation.

All tasks are treated as maximisation problems.

## Repository-Driven Process

The current repository separates the workflow into three data layers:

1. **Starter data (`.npy`)** in `data/initial_data/function_*/`
2. **Weekly working records (`.txt`)** in `queries/week1` to `queries/week13`
3. **Execution notebook** in `notebooks/bboWeeklyRunner.ipynb`

Core proposal logic is implemented in `black_box_optimizer.py`.

## Data Sources and Formats

### Initial datasets

- Path pattern: `data/initial_data/function_<k>/`
- Files:
	- `initial_inputs.npy`
	- `initial_outputs.npy`

These are the base observations used to start optimisation.

### Weekly datasets

- Path pattern: `queries/week<k>/`
- Files per function:
	- `function_1_inputs.txt` ... `function_8_inputs.txt`
	- `function_1_outputs.txt` ... `function_8_outputs.txt`
- Optional aggregate files:
	- `inputs.txt`
	- `outputs.txt`

The notebook reads per-function text files, parses them into NumPy arrays, and runs one proposal step per function.

## Optimisation Method in Code

The active optimiser is **Gaussian Process + Expected Improvement (EI)**:

- Surrogate: `GaussianProcessRegressor` with Matérn kernel (`nu=2.5`)
- Acquisition: EI with exploration parameter `xi=0.01`
- Candidate search: random sampling in `[0,1]^d` with best-EI selection
- Output formatting: clipped to `[0,1]` and rounded to 6 decimals

In the current implementation, `optimise_black_box(...)` proposes `x_next` values and prints them. It does **not** call the external black-box evaluator itself.

## Weekly Execution Steps

For each selected week folder:

1. Open `notebooks/bboWeeklyRunner.ipynb`.
2. Set `WEEK` (for example `week5`).
3. For each function 1 to 8:
	 - Load `function_<k>_inputs.txt` and `function_<k>_outputs.txt`
	 - Parse string-formatted arrays into NumPy arrays
	 - Run `optimise_black_box(..., max_queries=1)` to propose one new point
4. Submit proposed points via the project portal.
5. Receive scalar outputs and update the next week’s `queries/week*/` files.

## Reflection and Iteration

After each weekly run, record:

- Method used for candidate selection
- Exploration vs exploitation intent
- What changed after observing new outputs
- Planned adjustment for the next week

This ensures traceable decision-making and supports final reporting quality.

## Practical Notes

- `.npy` files are binary and should be loaded with `np.load(...)`.
- Weekly text files are parsed from array-like string representations in the notebook.
- Keep naming consistent (`function_<k>_inputs.txt`, `function_<k>_outputs.txt`) to avoid runner errors.

## Current Limitations

- No in-loop objective callback inside `optimise_black_box`.
- No automatic append of new weekly outputs within the optimiser function.
- Candidate search uses random EI maximisation, which may miss better optima in higher dimensions.

Despite these constraints, the setup is suitable for a transparent, reproducible weekly optimisation cycle aligned with the capstone submission format.
