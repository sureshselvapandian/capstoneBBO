from pathlib import Path

import numpy as np


def write_as_array_list(values, output_path: Path) -> None:
    text = "[" + ", ".join(repr(np.array(v)) for v in values) + "]"
    output_path.write_text(text, encoding="utf-8")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    function1_dir = repo_root / "initial_data" / "function_8"

    initial_inputs = np.load(function1_dir / "initial_inputs.npy")
    initial_outputs = np.load(function1_dir / "initial_outputs.npy")

    out_dir = Path(__file__).resolve().parent
    inputs_txt = out_dir / "function_8_initial_inputs.txt"
    outputs_txt = out_dir / "function_8_initial_outputs.txt"

    write_as_array_list(initial_inputs, inputs_txt)
    write_as_array_list(initial_outputs, outputs_txt)

    print(f"Saved: {inputs_txt}")
    print(f"Saved: {outputs_txt}")


if __name__ == "__main__":
    main()
