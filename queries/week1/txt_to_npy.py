from pathlib import Path

import numpy as np


def read_txt_arrays(txt_path: Path) -> list[np.ndarray]:
    content = txt_path.read_text(encoding="utf-8").strip()
    safe_globals = {"__builtins__": {}}
    safe_locals = {"array": np.array}
    parsed = eval(content, safe_globals, safe_locals)

    if not isinstance(parsed, list):
        raise ValueError("Expected a list of arrays in the input text file.")

    arrays: list[np.ndarray] = []
    for item in parsed:
        arrays.append(np.asarray(item, dtype=float))
    return arrays


def read_txt_outputs(txt_path: Path) -> list[float]:
    content = txt_path.read_text(encoding="utf-8").strip()
    safe_globals = {"__builtins__": {}}
    safe_locals = {"np": np}
    parsed = eval(content, safe_globals, safe_locals)

    if not isinstance(parsed, list):
        raise ValueError("Expected a list of numeric outputs in outputs.txt")

    return [float(value) for value in parsed]


def main() -> None:
    week1_dir = Path(__file__).resolve().parent
    inputs_txt_path = week1_dir / "inputs.txt"
    outputs_txt_path = week1_dir / "outputs.txt"

    arrays = read_txt_arrays(inputs_txt_path)
    if len(arrays) != 8:
        raise ValueError(f"Expected 8 arrays in inputs.txt, found {len(arrays)}")

    for index, arr in enumerate(arrays, start=1):
        npy_path = week1_dir / f"input_function_{index}.npy"
        np.save(npy_path, arr)

    outputs = read_txt_outputs(outputs_txt_path)
    if len(outputs) != 8:
        raise ValueError(f"Expected 8 values in outputs.txt, found {len(outputs)}")

    for index, value in enumerate(outputs, start=1):
        npy_path = week1_dir / f"output_function_{index}.npy"
        np.save(npy_path, np.array([value], dtype=float))

    print(f"Saved 16 files in: {week1_dir}")
    print("Input files:")
    for index in range(1, 9):
        print(f"- input_function_{index}.npy")
    print("Output files:")
    for index in range(1, 9):
        print(f"- output_function_{index}.npy")
    print(f"Dimensions: {[arr.shape[0] for arr in arrays]}")


if __name__ == "__main__":
    main()
