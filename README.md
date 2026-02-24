# Black-Box Optimisation Capstone Repository

## Project Summary

This repository contains code, weekly query records, and documentation for a black-box optimisation capstone across 8 functions (2D to 8D). The objective in each task is to maximise an unknown function under strict sequential-query constraints.

The workflow is iterative: use observed data to propose the next query, submit it externally, receive a scalar output, then update strategy for the next round.

## Current Repository Structure

```text
capstoneBBO/
├─ black_box_optimizer.py
├─ README.md
├─ Methodology.md
├─ Datasheet.md
├─ modelcard.md
├─ data/
│  └─ initial_data/
│     ├─ function_1/ ... function_8/
│     │  ├─ initial_inputs.npy
│     │  └─ initial_outputs.npy
├─ notebooks/
│  └─ bboWeeklyRunner.ipynb
└─ queries/
	 ├─ week1/ ... week13/
	 │  ├─ function_1_inputs.txt ... function_8_inputs.txt
	 │  ├─ function_1_outputs.txt ... function_8_outputs.txt
	 │  ├─ inputs.txt
	 │  └─ outputs.txt
```

### Key files and folders

- `black_box_optimizer.py`: GP + Expected Improvement helper used to propose next query points.
- `data/initial_data/`: starter `.npy` observations for each function.
- `queries/week*/`: per-week text records used by the weekly runner.
- `notebooks/bboWeeklyRunner.ipynb`: notebook used to run weekly proposal workflow.
- `Methodology.md`, `Datasheet.md`, `modelcard.md`: project documentation set.

## Data Format

- Inputs are continuous vectors within `[0, 1]`.
- Each function returns a single scalar output.
- Input dimension depends on function index:
	- Function 1–2: 2D
	- Function 3: 3D
	- Function 4–5: 4D
	- Function 6: 5D
	- Function 7: 6D
	- Function 8: 8D

## Weekly Workflow

1. Load current week inputs/outputs from `queries/weekX/`.
2. Fit surrogate(s) and propose one new query per function.
3. Submit queries to the capstone portal.
4. Receive new outputs and append them to next week’s data.
5. Repeat.

## How to Run

1. Open `notebooks/bboWeeklyRunner.ipynb`.
2. Set `WEEK` to the folder you want to process (for example `week5`).
3. Run the notebook cells to generate proposals.
4. Update weekly files after receiving portal outputs.

## Notes

- `.npy` files are binary NumPy files; load them with `np.load(...)` rather than opening as text.
- Weekly text parsing in the notebook expects the existing array-like formatting in `queries/week*/` files.

