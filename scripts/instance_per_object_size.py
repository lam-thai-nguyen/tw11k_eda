"""
Draw a figure showing the number of instances per object size
"""

from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image

SIZE_CATEGORIES = ("Tiny", "Small", "Medium", "Large")
AREA_THRESHOLDS = (16 * 16, 32 * 32, 96 * 96)


def main():
    data_dir = Path(__file__).resolve().parents[1] / "data"
    instance_counts = Counter()

    for split in ("train", "val"):
        labels_dir = data_dir / split / "labels"
        images_dir = data_dir / split / "images"
        for label_file in labels_dir.glob("*.txt"):
            image_file = images_dir / f"{label_file.stem}.jpg"
            with Image.open(image_file) as image:
                image_width, image_height = image.size

            with label_file.open(encoding="utf-8") as file:
                for line in file:
                    values = line.split()
                    if not values:
                        continue
                    if len(values) != 5:
                        raise ValueError(f"Invalid YOLO label in {label_file}: {line}")

                    box_width, box_height = map(float, values[3:5])
                    area = box_width * image_width * box_height * image_height
                    if area < AREA_THRESHOLDS[0]:
                        category = "Tiny"
                    elif area < AREA_THRESHOLDS[1]:
                        category = "Small"
                    elif area < AREA_THRESHOLDS[2]:
                        category = "Medium"
                    else:
                        category = "Large"
                    instance_counts[category] += 1

    counts = [instance_counts[category] for category in SIZE_CATEGORIES]

    plt.rcParams["svg.fonttype"] = "none"
    plt.figure(figsize=(8, 6))
    bars = plt.bar(SIZE_CATEGORIES, counts)
    for bar, count in zip(bars, counts):
        plt.annotate(
            str(count),
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
        )
    plt.xlabel("Object size")
    plt.ylabel("Count")
    plt.title("Number of instances per object size")
    plt.tight_layout()
    output_path = (
        Path(__file__).resolve().parents[1] / "output" / "instance_per_object_size.svg"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, format="svg")


if __name__ == "__main__":
    main()