import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from src.color import wavelength_to_rgb
from src.physics import calculate_intensity
from src.spectrum import calculate_quasi_monochromatic_pattern

def run_interactive() -> None:
    x = np.linspace(-0.03, 0.03, 4000)

    initial_n = 5
    initial_a = 20.0
    initial_d = 100.0
    initial_lambda = 550.0
    initial_spectrum_width = 0.0
    initial_l = 1.0

    intensity, image = calculate_quasi_monochromatic_pattern(
        x=x,
        slit_count=initial_n,
        slit_width=initial_a * 1e-6,
        slit_period=initial_d * 1e-6,
        central_wavelength_nm=initial_lambda,
        spectrum_width_nm=initial_spectrum_width,
        screen_distance=initial_l,
    )

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(11, 8),
        height_ratios=[1, 3],
    )

    plt.subplots_adjust(
        left=0.10,
        right=0.97,
        top=0.88,
        bottom=0.37,
        hspace=0.45,
    )

    rgb = wavelength_to_rgb(initial_lambda)
    image = np.tile(intensity, (80, 1))[:, :, np.newaxis] * rgb

    pattern_plot = axes[0].imshow(
        image,
        aspect="auto",
        extent=[x[0] * 1000, x[-1] * 1000, 0, 1],
        vmin=0,
        vmax=1,
    )

    axes[0].text(
        0.5,
        1.08,
        "Интерференционная картина",
        transform=axes[0].transAxes,
        ha="center",
        fontsize=14,
    )

    axes[0].set_yticks([])

    line_plot, = axes[1].plot(x * 1000, intensity)
    axes[1].set_xlabel("x, мм")
    axes[1].set_ylabel("Нормированная интенсивность")
    axes[1].grid(True)
    axes[1].set_ylim(-0.05, 1.05)

    ax_n = plt.axes([0.18, 0.26, 0.68, 0.03])
    ax_a = plt.axes([0.18, 0.215, 0.68, 0.03])
    ax_d = plt.axes([0.18, 0.17, 0.68, 0.03])
    ax_lambda = plt.axes([0.18, 0.125, 0.68, 0.03])
    ax_spectrum_width = plt.axes([0.18, 0.08, 0.68, 0.03])
    ax_l = plt.axes([0.18, 0.035, 0.68, 0.03])

    slider_n = Slider(ax_n, "N", 1, 10, valinit=initial_n, valstep=1)

    slider_a = Slider(
        ax_a,
        "a, мкм",
        5,
        100,
        valinit=initial_a,
        valstep=1,
    )

    slider_d = Slider(
        ax_d,
        "d, мкм",
        20,
        300,
        valinit=initial_d,
        valstep=5,
    )

    slider_lambda = Slider(
        ax_lambda,
        "λ, нм",
        380,
        750,
        valinit=initial_lambda,
        valstep=5,
    )

    slider_spectrum_width = Slider(
        ax_spectrum_width,
        "Δλ, нм",
        0,
        120,
        valinit=initial_spectrum_width,
        valstep=5,
    )

    slider_l = Slider(
        ax_l,
        "L, м",
        0.2,
        3.0,
        valinit=initial_l,
        valstep=0.1,
    )

    def update(_):
        slit_count = int(slider_n.val)
        slit_width = slider_a.val * 1e-6
        actual_d = max(slider_d.val, slider_a.val)
        slit_period = actual_d * 1e-6
        wavelength = slider_lambda.val * 1e-9
        screen_distance = slider_l.val

        new_intensity, new_image = calculate_quasi_monochromatic_pattern(
            x=x,
            slit_count=slit_count,
            slit_width=slit_width,
            slit_period=slit_period,
            central_wavelength_nm=slider_lambda.val,
            spectrum_width_nm=slider_spectrum_width.val,
            screen_distance=screen_distance,
        )

        pattern_plot.set_data(new_image)
        line_plot.set_ydata(new_intensity)

        info_text.set_text(
            f"N = {slit_count}    "
            f"a = {round(slider_a.val)} μm    "
            f"d = {round(actual_d)} μm    "
            f"λ₀ = {round(slider_lambda.val)} nm    "
            f"Δλ = {round(slider_spectrum_width.val)} nm    "
            f"L = {slider_l.val:.1f} m"
        )

        fig.canvas.draw_idle()

    slider_n.on_changed(update)
    slider_a.on_changed(update)
    slider_d.on_changed(update)
    slider_lambda.on_changed(update)
    slider_spectrum_width.on_changed(update)
    slider_l.on_changed(update)

    info_text = fig.text(
        0.5,
        0.985,
        "",
        ha="center",
        va="center",
        fontsize=11,
    )

    update(None)
    plt.show()