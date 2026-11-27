"""
Draw a figure showing the number of instances per class
"""

from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt

CLASS_NAMES = [
    "warning_triangle",
    "warning_others",
    "mandatory_others",
    "mandatory_triangle",
    "mandatory_circle",
    "mandatory_rectangle",
    "restriction_circle",
    "restriction_rectangle",
    "restriction_others",
    "limit_circle",
    "guidance_rectangle",
    "guidance_others",
    "guidance_circle",
    "guidance_arrow",
    "assistance_rectangle",
    "barricade_rectangle",
    "construction_diamond",
    "signal",
    "danger",
    "limit_others",
    "warning_rectangle",
]


def main():
    data_dir = Path(__file__).resolve().parents[1] / "data"
    labels_dirs = [data_dir / split / "labels" for split in ("train", "val")]
    instance_counts = Counter()

    for labels_dir in labels_dirs:
        for label_file in labels_dir.glob("*.txt"):
            with label_file.open(encoding="utf-8") as file:
                for line in file:
                    values = line.split()
                    if values:
                        class_id = int(values[0])
                        if not 0 <= class_id < len(CLASS_NAMES):
                            raise ValueError(
                                f"Class ID {class_id} in {label_file} is out of range"
                            )
                        instance_counts[class_id] += 1

    sorted_classes = sorted(
        range(len(CLASS_NAMES)),
        key=lambda class_id: instance_counts[class_id],
        reverse=True,
    )
    class_names = [CLASS_NAMES[class_id] for class_id in sorted_classes]
    counts = [instance_counts[class_id] for class_id in sorted_classes]

    plt.rcParams["svg.fonttype"] = "none"
    plt.figure(figsize=(14, 6))
    bars = plt.bar(class_names, counts)
    for bar, count in zip(bars, counts):
        plt.annotate(
            str(count),
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
        )
    plt.xlabel("Class")
    plt.ylabel("Count")
    plt.title("Number of instances per class")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    output_path = (
        Path(__file__).resolve().parents[1] / "output" / "instance_per_class.svg"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, format="svg")


if __name__ == "__main__":
    main()
