"""
Print how many images are in each dataset folder and its class subfolders,
then check that no filename appears in more than one of train, validation
and test.

Covers dataset/fetched_dataset, dataset/train, dataset/validation and
dataset/test. Run from the project root:  python count_images.py
"""
from itertools import combinations
from pathlib import Path

DATASET = Path("dataset")
FOLDERS = ["fetched_dataset", "train", "validation", "test"]
SPLITS = ["train", "validation", "test"]
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def count_images(folder: Path) -> int:
    return sum(
        1 for f in folder.rglob("*")
        if f.is_file() and f.suffix.lower() in IMAGE_SUFFIXES
    )


def image_names(folder: Path) -> set[str]:
    return {
        f.name for f in folder.rglob("*")
        if f.is_file() and f.suffix.lower() in IMAGE_SUFFIXES
    }


def check_split_overlap() -> None:
    """Report any filename shared between train, validation and test."""
    print("Overlap check (by filename):")
    names = {s: image_names(DATASET / s) for s in SPLITS if (DATASET / s).is_dir()}
    clean = True
    for a, b in combinations(names, 2):
        shared = names[a] & names[b]
        label = f"{a} vs {b}"
        if shared:
            clean = False
            examples = ", ".join(sorted(shared)[:5])
            print(f"  {label:<24} {len(shared):>7,} shared  e.g. {examples}")
        else:
            print(f"  {label:<24} {'0':>7} shared")
    if clean:
        print("  OK: no image filename appears in more than one split.")
    else:
        print("  WARNING: some images appear in more than one split.")


def main() -> None:
    grand_total = 0
    for name in FOLDERS:
        folder = DATASET / name
        if not folder.is_dir():
            print(f"{name}: folder not found")
            print()
            continue

        subfolders = sorted(p for p in folder.iterdir() if p.is_dir())
        total = 0
        print(f"{name}:")
        for sub in subfolders:
            n = count_images(sub)
            total += n
            print(f"  {sub.name:<18} {n:>7,}")
        loose = count_images(folder) - total
        if loose:
            print(f"  {'(not in subfolder)':<18} {loose:>7,}")
            total += loose
        print(f"  {'total':<18} {total:>7,}")
        print()
        grand_total += total

    print(f"All folders combined: {grand_total:,} images")
    print()
    check_split_overlap()


if __name__ == "__main__":
    main()
