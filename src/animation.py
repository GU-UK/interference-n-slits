import imageio
import matplotlib.pyplot as plt
import numpy as np

from src.spectrum import calculate_quasi_monochromatic_pattern


DEFAULT_PARAMETERS = {
    "slit_count": 5,
    "slit_width_um": 20.0,
    "slit_period_um": 100.0,
    "central_wavelength_nm": 550.0,
    "spectrum_width_nm": 0.0,
    "screen_distance_m": 1.0,
}


def export_animation(
    parameter: str,
    start: float,
    end: float,
    duration: float,
    filename: str = "assets/interference.gif",
    frame_count: int = 40,
) -> None:
    x = np.linspace(-0.03, 0.03, 4000)
    frames = []

    values = np.linspace(start, end, frame_count)

    for value in values:
        params = DEFAULT_PARAMETERS.copy()
        params[parameter] = value

        intensity, image = calculate_quasi_monochromatic_pattern(
            x=x,
            slit_count=int(round(params["slit_count"])),
            slit_width=params["slit_width_um"] * 1e-6,
            slit_period=max(
                params["slit_period_um"],
                params["slit_width_um"],
            )
            * 1e-6,
            central_wavelength_nm=params["central_wavelength_nm"],
            spectrum_width_nm=params["spectrum_width_nm"],
            screen_distance=params["screen_distance_m"],
        )

        fig = plt.figure(figsize=(10, 2))

        plt.imshow(
            image,
            aspect="auto",
            extent=[-30, 30, 0, 1],
        )

        plt.title(_make_title(parameter, value))
        plt.axis("off")

        fig.canvas.draw()

        frame = np.asarray(fig.canvas.renderer.buffer_rgba())
        frames.append(frame)

        plt.close(fig)

    fps = frame_count / duration

    imageio.mimsave(
        filename,
        frames,
        fps=fps,
        loop=0,
    )

    print(f"GIF сохранён: {filename}")


def _make_title(parameter: str, value: float) -> str:
    titles = {
        "slit_count": f"N = {int(round(value))}",
        "slit_width_um": f"a = {value:.1f} мкм",
        "slit_period_um": f"d = {value:.1f} мкм",
        "central_wavelength_nm": f"λ₀ = {value:.0f} нм",
        "spectrum_width_nm": f"Δλ = {value:.0f} нм",
        "screen_distance_m": f"L = {value:.2f} м",
    }

    return titles.get(parameter, f"{parameter} = {value:.2f}")