from pathlib import Path


def main() -> None:
    folder = Path(__file__).resolve().parent

    renamed = []
    for path in folder.iterdir():
        if not path.is_file():
            continue
        if "initial_" not in path.name:
            continue

        new_name = path.name.replace("initial_", "")
        target = path.with_name(new_name)

        if target.exists():
            print(f"Skip (target exists): {target.name}")
            continue

        path.rename(target)
        renamed.append((path.name, target.name))

    if not renamed:
        print("No files renamed.")
        return

    print("Renamed files:")
    for old_name, new_name in renamed:
        print(f"- {old_name} -> {new_name}")


if __name__ == "__main__":
    main()
