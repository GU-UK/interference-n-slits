import matplotlib.pyplot as plt
import numpy as np


def show_result(x: np.ndarray, intensity: np.ndarray, title: str) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), height_ratios=[1, 3])

    image = np.tile(intensity, (80, 1))

    axes[0].imshow(
        image,
        cmap="gray",
        aspect="auto",
        extent=[x[0] * 1000, x[-1] * 1000, 0, 1],
    )
    axes[0].set_yticks([])
    axes[0].set_title("Interference pattern on screen")

    axes[1].plot(x * 1000, intensity)
    axes[1].set_xlabel("x, mm")
    axes[1].set_ylabel("Normalized intensity")
    axes[1].set_title(title)
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()